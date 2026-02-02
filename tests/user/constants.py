GET_ALL_PATH = "/users/"
INVALID_LIMIT = {
    "limit": -1,
}
INVALID_LIMIT2 = {
    "limit": 0,
}
INVALID_OFFSET = {
    "offset": -1,
}
INVALID_OFFSET2 = {
    "offset": 2 ** 32 + 1,
}
VALID_MULTI_GET_PARAMS = {
    "limit": 15,
    "offset": 0,
}
