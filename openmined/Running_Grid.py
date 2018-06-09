
# coding: utf-8

# # Distributed model training with PyTorch's `torch.autograd` on Grid
# 
# #### For Siraj's Distributed Apps Course
# 

# In[1]:


import torch # THis line should NOT be run after instantiating TorchClient
import torch.nn as nn
from torch.autograd import Variable
from grid.clients.torch import TorchClient
import numpy as np
import re

# instantiate client
client = TorchClient(verbose=False)


# ## First Steps

# The first step is to find out which nodes are connected to the Grid network. After this we can choose who to run the computations with.

# In[2]:


client.print_network_stats()


# In[3]:


compute_nodes = [x for x in client if re.match('compute:', x)]
assert len(compute_nodes) > 0

print(compute_nodes)


# In[4]:


compute_nodes = compute_nodes[::-1]


# In[5]:


compute_nodes


# In[6]:


laptop = compute_nodes[0]


# ### Remote Tensor Ops

# In[7]:


x = torch.FloatTensor([[1,1],[2,2]])
x.send_(laptop)
y = x * x
y.get_()


# ### Beyond gradient-based models
# 
# Tensor computation is sufficient for training most gradient-based models, but it's not convenient for doing so when backpropagation is involved.  To solve this, we'll want to use automatic differentiation using the Variable class from `torch.autograd`.

# Here are some useful Grid-specific attributes that are useful for these purposes. Since we want to use autograd, we'll do so with Variables instead of tensors, but all the usual Tensor types have these attributes too.

# In[8]:


# Note: Variable is now a purely internal class in PyTorch v0.4.0,
#       but Grid currently depends on v0.3.1.
#       This will be updated as soon as possible.

x = Variable(torch.FloatTensor([[1,1],[2,2]]), requires_grad=True)
y = Variable(torch.FloatTensor([[1,1],[2,2]]), requires_grad=True)

print(x)

print('======\nGrid-specific attributes\n======')
print('owners: {}'.format(x.owners))
print('id: {}'.format(x.id))
print('is_pointer: {}'.format(x.is_pointer))


# #### Grid attributes:
# - The `owners` attribute tells us where the tensor's data lives.
# - The `id` attribute is a way for each machine's instance of Grid to track which Torch objects they're holding locally, allowing different machines to request access to different objects.  This also allows each worker to know which tensors they need to perform computations on.
# - The `is_pointer` attribute tells us whether or not the object we're referring to is local or remote.  If it's local (is_pointer is False), we'll execute normal PyTorch code on it.  Otherwise, we'll send our command to the owner machine and have it perform the computation we want over there.

# Now we can send our Variables like we did with the first tensor.

# In[9]:


x.send_(laptop)
y.send_(laptop)

print(x)

print('======\nGrid-specific attributes\n======')
print('owners: {}'.format(x.owners))
print('id: {}'.format(x.id))
print('is_pointer: {}'.format(x.is_pointer))


# The location is different (we're now using a compute node with a different worker ID), and the `is_pointer` attribute changed to True.  The data is no longer on this machine; it's now on the worker machine.

# We'll demonstrate some remote computation below:

# In[10]:


z = x.matmul(y)


# We can check out the result's attributes like we did for `x` and `y` above.

# In[11]:


print(z)

print('======\nGrid-specific attributes\n======')
print('owners: {}'.format(z.owners))
print('id: {}'.format(z.id))
print('is_pointer: {}'.format(z.is_pointer))


# #### Why is this notable?

# We didn't have to change anything in our PyTorch code.  The command `matmul` is identical to the normal PyTorch command, but the computation is being performed elsewhere.
# 
# This example was also NOT cherry-picked; theoretically any method or function that inputs and outputs Tensor/Variable objects can be used in this exact same way, as long as those objects are stored somewhere on Grid and we have a local pointer to those objects.
# 
# Although the computation result is on the other machine, we still have access to a local pointer for the Variable.  We can use that pointer in future computations, chaining together commands for remote machines without having to retrieve and send the underlying data between each command. For example:

# In[12]:


z_sum = z.sum()


# #### Checking derivatives

# We used Variables so that we can take advantage of autograd.  Let's make sure that works, by taking the derivative of `z_sum` with respect to `x` and `y`:

# In[13]:


z_sum.backward()


# The derivatives with respect to `x` and `y` are now stored in `x.grad` and `y.grad`, but we'll need to retrieve `x` and `y` to access those.  That's okay for this use case, since we're not concerned about data privacy right now.  Figuring out how to call `get_` on the grad itself would be another useful contribution!

# In[14]:


x.get_()
y.get_()

print(x.grad)
print(y.grad)


# We've now computed derivatives on a remote machine, and we did so interactively with a dynamic computation graph over a peer-to-peer network!

# # Training a model with distributed gradient descent

# Currently, IPFS has some limitations around how much data can be transferred in one block.  They've introduced a sharding mechanism to get around this ([see here](https://github.com/ipfs/go-ipfs/pull/3042)), but it's not currently being used in Grid. 
# 
# We'll use Data with relatively low dimensionality -- the [Boston housing prices dataset](https://www.kaggle.com/c/boston-housing/data).

# In[15]:


from keras.datasets import boston_housing


# In[16]:


(X, y), (X_test, y_test) = boston_housing.load_data()


# In[17]:


X = torch.from_numpy(X).type(torch.FloatTensor)
y = torch.from_numpy(y).type(torch.FloatTensor)
X_test = torch.from_numpy(X_test).type(torch.FloatTensor)
y_test = torch.from_numpy(y_test).type(torch.FloatTensor)


# In[18]:


# preprocessing
mean = X.mean(0, keepdim=True)
dev = X.std(0, keepdim=True)
mean[:, 3] = 0. # the feature at column 3 is binary,
dev[:, 3] = 1.  # so I'd rather not standardize it
X = (X - mean) / dev
X_test = (X_test - mean) / dev


# #### Hyperparameters

# In[20]:


# training
batch_size = 8
learning_rate = .01
epochs = 5
update_master_every = 3

# architecture
input_shape = X.shape[1]
first_neurons = 64
second_neurons = 32
try: # will work for multivariate regression tasks too
    dep_vars = y.size(1)
except RuntimeError:
    dep_vars = 1


# #### PyTorch utilities for supplying data to models

# In[21]:


from torch.utils.data import TensorDataset, DataLoader


# In[22]:


train = TensorDataset(X, y)
test = TensorDataset(X_test, y_test)


# In[23]:


tr_load = DataLoader(train, batch_size = 8, drop_last=True)
ts_load = DataLoader(test, batch_size = 8, drop_last=True)


# #### Allocating training batches to each worker
# 
# Once we send batches out to participating workers, they won't need to move around for the rest of training -- they'll only be sharing the model.  Our client machine will play the role of Parameter Server.  This is known as "data parallelism" (as opposed to "model parallelism").

# In[24]:


get_ipython().run_cell_magic('time', '', '\nallocated = []\n\nfor (ix, (x_i, y_i)) in enumerate(tr_load):\n    x_i = Variable(x_i, requires_grad = True)\n    y_i = Variable(y_i, requires_grad = True)\n    x_i.send_(compute_nodes[ix % len(compute_nodes)])\n    y_i.send_(compute_nodes[ix % len(compute_nodes)])\n    allocated.append((x_i, y_i))')


# In[25]:


len(allocated)


# #### Setting up the model parameters.

# In[27]:


W_0 = nn.Parameter(torch.FloatTensor(input_shape, first_neurons))
W_1 = nn.Parameter(torch.FloatTensor(first_neurons, second_neurons))
W_2 = nn.Parameter(torch.FloatTensor(second_neurons, dep_vars))

# initialize properly
relu_gain = nn.init.calculate_gain('relu')
lin_gain = nn.init.calculate_gain('linear')

nn.init.xavier_normal(W_0, gain=relu_gain)
nn.init.xavier_normal(W_1, gain=relu_gain)
nn.init.xavier_normal(W_2, gain=lin_gain)

print('Network parameters initialized.')


# Architecture helpers

# In[28]:


def relu(x):
    """Rectified linear activation"""
    return torch.clamp(x, min=0.)

def linear(x, w):
    """Linear transformation of x by w"""
    return torch.matmul(x,w)

def mse(y_hat, y_true):
    """Mean-squared error"""
    return torch.mean(torch.pow(y_hat - y_true, 2), dim=0, keepdim=True)


# Gradient update helpers

# In[29]:


def average_grads(grads):
    """Average a sequence of gradients"""
    return torch.mean(torch.cat(grads))

def update_params(param, grad, alpha):
    """Update parameter tensor with standard mini-batch gradient descent"""
    return param - alpha * grad

def reset_flags(param):
    """Resets flags for a Parameter that's experienced an in-place operation"""
    param.requires_grad = True
    param.volatile = False


# #### Main training loop

# In[30]:


# Initialize gradient buffers
W_0_grads = []
W_1_grads = []
W_2_grads = []

# Loop over epochs
for epoch in range(epochs):

    # Loop over distributed batches
    for ix, (x_i, y_i) in enumerate(allocated):
        # Broadcast current weights to workers
        W_0_clones = [W_0.clone().send_(node) for node in compute_nodes]
        W_1_clones = [W_1.clone().send_(node) for node in compute_nodes]
        W_2_clones = [W_2.clone().send_(node) for node in compute_nodes]

        # Pull pointers from clone list
        W_0_tmp = W_0_clones[ix % len(compute_nodes)]
        W_1_tmp = W_1_clones[ix % len(compute_nodes)]
        W_2_tmp = W_2_clones[ix % len(compute_nodes)]

        # Forward pass
        act_0 = relu(linear(x_i, W_0_tmp))
        act_1 = relu(linear(act_0, W_1_tmp))
        y_hat = linear(act_1, W_2_tmp).view(-1)

        # Calculate MSE loss and perform backprop
        y_i = y_i.type_as(y_hat) # type-safety
        loss = mse(y_hat, y_i)
        loss.backward()

        # Recall parameters
        W_0_tmp.get_()
        W_1_tmp.get_()
        W_2_tmp.get_()

        # Store parameter grads
        W_0_grads.append(W_0_tmp.grad)
        W_1_grads.append(W_1_tmp.grad)
        W_2_grads.append(W_2_tmp.grad)

        # Update master parameters
        if ix % update_master_every == 0:
            W_0_grad = average_grads(W_0_grads)
            W_1_grad = average_grads(W_1_grads)
            W_2_grad = average_grads(W_2_grads)

            W_0 = update_params(W_0, W_0_grad, alpha=learning_rate)
            W_1 = update_params(W_1, W_1_grad, alpha=learning_rate)
            W_2 = update_params(W_2, W_2_grad, alpha=learning_rate)

            # We've overridden Variables in-place, which breaks the computation graph internally
            # This is intentional, but this needs to be cleaned up a bit to be able to keep going
            reset_flags(W_0)
            reset_flags(W_1)
            reset_flags(W_2)
            
            # Cleaning out parameter server grad buffers
            W_0_grads = []
            W_1_grads = []
            W_2_grads = []
            

    print("Epoch {} done!".format(epoch + 1))

