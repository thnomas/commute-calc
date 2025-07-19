import json

test_info = {
   "access_token": "dummy",
   "refresh_token": "dummy",
   "expires_in": "43152"
}

def write_to_file(tokens, filename='tokens.json'):
   with open(filename, 'w') as f:
       json.dump(tokens, f)

def read_from_file(filename='tokens.json'):
   with open(filename) as f:
       return json.load(f)

def check_token_expiration(info):
   if int(info["expires_in"]) <= 0:
       print("ExPiReD")
       return True
   return False
  
# read_from_file()
# info = read_from_file()
# expired = check_token_expiration(info)

if __name__ == "__main__":
   write_to_file(test_info, filename='tokens_test.json')
   print(f"Token info written to tokens_test.json")
   print(read_from_file(filename='tokens_test.json'))
   check_token_expiration(test_info)