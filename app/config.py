import os
from dotenv import load_dotenv

load_dotenv()

TOGETHER_AI_API_KEY = os.getenv("TOGETHER_AI_API_KEY")
CRYPTO_API_URL = "https://api.coincap.io/v2/assets"
SUPPORTED_CRYPTO = [
    "bitcoin", "ethereum", "litecoin", "ripple", "bitcoin-cash",
    "cardano", "polkadot", "chainlink", "binancecoin", "tether",
    "dogecoin", "solana", "avalanche", "uniswap", "stellar",
    "vechain", "tron", "tezos", "monero", "aave",
    "filecoin", "theta", "elrond", "cosmos", "algorand",
    "eos", "iota", "neo", "dash", "zcash",
    "maker", "compound", "yearn-finance", "pancakeswap",
    "terra-luna", "shiba-inu", "fantom", "decentraland",
    "enjin-coin", "sushiswap", "harmony", "near",
    "the-graph", "quant", "chiliz", "loopring", "bitcoin-sv",
    "waves", "hedera-hashgraph", "basic-attention-token",
    "zilliqa", "kava", "celo", "kusama"
]

CACHE_TTL=60