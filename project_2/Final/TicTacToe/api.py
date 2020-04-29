import requests
import json

user = {848: {'x-api-key': '5fc0a40bd471dd9ed9d0', 'userId': '848'},
        923: {'x-api-key': '691bd185db168dfdfca4', 'userId': '923'},
        933: {'x-api-key': '1c7f5baf36bdf3bbc438', 'userId': '933'},
        934: {'x-api-key': '691bd185db168dfdfca4', 'userId': '934'}}


class Api:
    def __init__(self, user_id, team_id):
        self.COM_HEADER = {'Host': 'www.notexponential.com',
                           'Accept': 'text/html',
                           'Connection': 'keep-alive',
                           'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                                         'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'}

        self.COM_HEADER.update(user[user_id])
        self.URL = 'http://www.notexponential.com/aip2pgaming/api/index.php'

        self.TEAM_ID = team_id
        self.game_id = None

    @staticmethod
    def check_response_validity(res):
        # print(res.text)
        if res.status_code != 200:
            raise Exception('Http request fail. Status code: ' + str(res.status_code) + '\nContent: ' + res.text)
        js = json.loads(res.text)
        if js['code'] != 'OK':
            raise Exception('Game request fail. Reason: ' + js['message'])

    def get_team_member(self):
        # To test if connection with server is OK. No use for game playing
        cus_para = {'type': 'team', 'teamId': self.TEAM_ID}
        response = requests.get(self.URL, headers=self.COM_HEADER, params=cus_para)
        self.check_response_validity(response)
        return json.loads(response.text)['userIds']

    def get_my_game(self):
        cus_data = {'type': 'myGames'}
        response = requests.get(self.URL, headers=self.COM_HEADER, params=cus_data)
        self.check_response_validity(response)
        my_games = json.loads(response.text)['myGames']
        return my_games

    def set_game_id(self, game_id):
        # If code execution stops during a game. You can use this to continue playing that game
        self.game_id = game_id

    def start_with(self, str_other_team_id):
        # Start a new game with other team. Returns the GameID upon success
        cus_data = {'type': 'game', 'gameType': 'TTT', 'teamId1': self.TEAM_ID, 'teamId2': str_other_team_id}
        response = requests.post(self.URL, headers=self.COM_HEADER, data=cus_data)
        self.check_response_validity(response)
        self.game_id = json.loads(response.text)['gameId']

    def make_move(self, x, y):
        # Make a move on board. (x,y) is (row, col), index starting from 0
        cus_data = {'type': 'move', 'gameId': self.game_id, 'teamId': self.TEAM_ID, 'move': str(x) + ',' + str(y)}
        response = requests.post(self.URL, headers=self.COM_HEADER, data=cus_data)
        self.check_response_validity(response)

    def get_board(self):
        # Return board in 2D list. One cell can only contain char O, X, -.
        # O is the piece of first player, X second player, - empty cell.
        cus_para = {'type': 'boardString', 'gameId': self.game_id}
        response = requests.get(self.URL, headers=self.COM_HEADER, params=cus_para)
        self.check_response_validity(response)
        # turn string into 1-d list
        ls_string = json.loads(response.text)['output']
        ls_board = []
        str2num_dict = {'-': 0, 'X': 1, 'O': -1}
        for c in ls_string:
            if c in str2num_dict:
                ls_board.append(str2num_dict[c])
        return ls_board


if __name__ == '__main__':
    A = Api(848, 1201)
    # game_id = A.start_with(1216)
    # r1 = A.get_team_member()
    # A.set_game_id(50)
    r2 = A.get_my_game()
    print(r2)
    # r3 = A.get_board()
