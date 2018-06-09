
export const DEFAULT_CHAIN = 1337;

export const chains = {
  dev: {
    id: 1337,
    hub: '0x215a47b255f8636d8b44a807ae1dddbca7be10a7',
    server: 'https://mainxw.iex.ec:443',
    name: 'dev',
  },
  mainnet: {
    server: 'https://mainxw.iex.ec:443',
    name: 'mainnet',
    id: 1,
  },
  ropsten: {
    server: 'https://testxw.iex.ec:443',
    name: 'ropsten',
    id: 3,
  },
  rinkeby: {
    server: 'https://testxw.iex.ec:443',
    name: 'ropsten',
    id: 4,
  },
  kovan: {
    server: 'https://testxw.iex.ec:443',
    name: 'kovan',
    id: 42,
    hub: '0x12b92a17b1ca4bb10b861386446b8b2716e58c9b',
    api: '0x58cde9db0d95c8b6122d72a90c0b10a6e01adf6d',
  },
};
chains['1'] = chains.mainnet;
chains['3'] = chains.ropsten;
chains['4'] = chains.rinkeby;
chains['42'] = chains.kovan;
chains['1337'] = chains.dev;

export const chainsMap = {
  mainnet: '1',
  1: 'mainnet',
  ropsten: '3',
  3: 'ropsten',
  rinkeby: '4',
  4: 'rinkeby',
  kovan: '42',
  42: 'kovan',
  dev: '1137',
  1337: 'dev',
};


export const chainNames = ['mainnet', 'ropsten', 'rinkeby', 'kovan', 'dev'];
export const chainIDs = ['1', '3', '4', '42', '1337'];
