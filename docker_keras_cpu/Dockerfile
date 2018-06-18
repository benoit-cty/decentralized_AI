FROM ubuntu:16.04
# Based on Waleed Abdulla work
MAINTAINER Benoit Courty <nospam@gmail.fr>

# Supress warnings about missing front-end. As recommended at:
# http://stackoverflow.com/questions/22466255/is-it-possibe-to-answer-dialog-questions-when-installing-under-docker
ARG DEBIAN_FRONTEND=noninteractive

# Essentials: developer tools, build tools, OpenBLAS
RUN apt-get update && apt-get install -y --no-install-recommends \
    apt-utils git curl vim unzip openssh-client wget \
    build-essential cmake \
    libopenblas-dev && apt-get clean -y

#
# Python 3.5
#
# For convenience, alias (but don't sym-link) python & pip to python3 & pip3 as recommended in:
# http://askubuntu.com/questions/351318/changing-symlink-python-to-python3-causes-problems
RUN apt-get install -y --no-install-recommends python3.5 python3.5-dev python3-pip python3-tk && apt-get clean -y && \
    pip3 install --no-cache-dir --upgrade pip setuptools && \
    echo "alias python='python3'" >> /root/.bash_aliases && \
    echo "alias pip='pip3'" >> /root/.bash_aliases
# Pillow and it's dependencies
RUN apt-get install -y --no-install-recommends libjpeg-dev zlib1g-dev && \
    pip3 --no-cache-dir install Pillow
# Science libraries and other common packages
RUN pip3 --no-cache-dir install \
    numpy scipy  scikit-image  matplotlib Cython
#sklearn requests pandas

#
# Tensorflow 1.6.0 - CPU
#
RUN pip3 install --no-cache-dir --upgrade tensorflow

# Expose port for TensorBoard
#EXPOSE 6006

#
# OpenCV 3.4.1
#
# Dependencies
RUN apt-get install -y --no-install-recommends \
    libjpeg8-dev libtiff5-dev libjasper-dev libpng12-dev \
    libavcodec-dev libavformat-dev libswscale-dev libv4l-dev libgtk2.0-dev \
    liblapacke-dev checkinstall
# Get source from github
RUN git clone -b 3.4.1 --depth 1 https://github.com/opencv/opencv.git /usr/local/src/opencv
# Compile
RUN cd /usr/local/src/opencv && mkdir build && cd build && \
    cmake -D CMAKE_INSTALL_PREFIX=/usr/local \
          -D BUILD_TESTS=OFF \
          -D BUILD_PERF_TESTS=OFF \
          -D PYTHON_DEFAULT_EXECUTABLE=$(which python3) \
          .. && \
    make -j"$(nproc)" && \
    make install && \
    cd .. && rm -rf /usr/local/src/opencv

#
# Keras 2.1.5
#
RUN pip3 install --no-cache-dir --upgrade h5py pydot_ng keras

#
# PyCocoTools
#
# Using a fork of the original that has a fix for Python 3.
# I submitted a PR to the original repo (https://github.com/cocodataset/cocoapi/pull/50)
# but it doesn't seem to be active anymore.
RUN pip3 install --no-cache-dir git+https://github.com/waleedka/coco.git#subdirectory=PythonAPI

RUN pip3 --no-cache-dir install imgaug IPython

# Set matplotlib to headless mode
RUN mkdir -p /root/.config/matplotlib/ && echo "backend : Agg" > /root/.config/matplotlib/matplotlibrc

# Install Mask_RCNN
#RUN  git clone --depth 1  https://github.com/matterport/Mask_RCNN.git /usr/local/src/Mask_RCNN
RUN  git clone https://github.com/gtgalone/Mask_RCNN.git /usr/local/src/Mask_RCNN && \
   cd /usr/local/src/Mask_RCNN && git checkout fix-keras-engine-topology &&  rm -rf /usr/local/src/Mask_RCNN/.git  && \
   cd /usr/local/src/Mask_RCNN && $(which python3) setup.py install



RUN wget --quiet https://github.com/matterport/Mask_RCNN/releases/download/v2.0/mask_rcnn_coco.h5 -O /usr/local/src/Mask_RCNN/mask_rcnn_coco.h5

# Clean : useless as Docker will kept original files in history
#RUN rm -rf /usr/local/src/opencv
# /build
#    && make clean
RUN apt-get purge -y --no-install-recommends \
    apt-utils git curl vim unzip openssh-client wget \
    build-essential cmake \
    libopenblas-dev
#RUN rm -rf /usr/local/src/Mask_RCNN/.git

WORKDIR "/usr/local/src/Mask_RCNN/samples"
ADD maskrcnn.py /usr/local/src/Mask_RCNN/samples
# CMD ["/bin/bash"]
ENTRYPOINT ["/bin/bash", "-c",  "/usr/local/src/Mask_RCNN/samples/maskrcnn.py \"$@\"", "--"]
