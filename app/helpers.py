import os
import requests
import random
import html
import time
import pickle



def gen_session_token():

    session_token_data = requests.get("https://opentdb.com/api_token.php?command=request").json()

    token = session_token_data["token"]

    return token



def random_question(difficulty, provider=None, open_session_token=None):

    if provider == "jep":
        return random_jep(difficulty)
    elif provider == "open":
        return random_open(difficulty, open_session_token)
    else:

        if random.random() < 0.5:
            return random_jep(difficulty)
        else:
            return random_open(difficulty, open_session_token)


# for jservice
def max_offsets():
    # {100: 9745, 200: 30904, 300: 9284, 400: 29955, 500: 8873, 600: 20312, 800: 19809, 1000: 19837}

    print("getting jservice max offsets")
    values = [100,200,300,400,500,600,800,1000]

    off_dict = {}

    for val in values:
        print(val)
        offset = 0

        while len(requests.get(f"https://jservice.io/api/clues?value={val}&offset={offset}").json()) == 100:

            offset += 100

        offset += len(requests.get(f"https://jservice.io/api/clues?value={val}&offset={offset}").json())

        off_dict[val] = offset

    pickle.dump(off_dict, open("jep_max_offsets.p", "wb"))
    return off_dict


def random_jep(difficulty):

    if os.path.exists("jep_max_offsets.p"):
        max_offs = pickle.load(open("jep_max_offsets.p", "rb"))
    else:
        max_offs = max_offsets()

    difficulty_values = {"easy": [100, 200, 400], "medium": [300, 400, 600, 800], "hard": [500, 1000]}

    val = random.choice(difficulty_values[difficulty])
    q_data = requests.get(f"https://jservice.io/api/clues?value={val}&offset={random.randrange(max_offs[val])}").json()

    return {"category": html.unescape(q_data[0]["category"]["title"]), 
            "question": html.unescape(q_data[0]["question"]), 
            "answer": html.unescape(q_data[0]["answer"]), 
            "difficulty": difficulty, 
            "value": val, 
            "provider": "jep"}



def random_open(difficulty, token, BLACKLIST_CATEGORY_IDS = {15, 16, 29, 31, 32}):

    #get all categories from api
    category_resp = requests.get("https://opentdb.com/api_category.php").json()["trivia_categories"]

    #get category id numbers
    category_id_nums = {i["id"] for i in category_resp}

    #get id:name for each category
    category_ids = {i["id"]:i["name"] for i in category_resp}


    #create set of ids we do want
    WHITELIST_CATEGORY_IDS = category_id_nums - BLACKLIST_CATEGORY_IDS

    #remove unwanted categories from dictionary
    [category_ids.pop(key) for key in list(BLACKLIST_CATEGORY_IDS)]

    rand_category = random.choice(list(WHITELIST_CATEGORY_IDS))

    valid = False
    while not valid:
        q_data = requests.get(f"https://opentdb.com/api.php?amount=1&category={rand_category}&token={token}").json()

        q = html.unescape(q_data["results"][0]["question"])
        if q.lower().find("which of these") > -1 or q.lower().find("which of the following") > -1 or q.lower().find("which one of these") > -1:
            continue
        else:
            valid = True

    q = html.unescape(q_data["results"][0]["question"])
    if html.unescape(q_data["results"][0]["type"]) == "boolean":
            q = "True/False - " + q

    return {"category": html.unescape(q_data["results"][0]["category"]), 
            "question": q, 
            "answer": html.unescape(q_data["results"][0]["correct_answer"]), 
            "incorrect_answers": html.unescape(q_data["results"][0]["incorrect_answers"]),
            "difficulty": difficulty, 
            "type": html.unescape(q_data["results"][0]["type"]), 
            "provider": "open"}



def generate_game(rounds=4, num_questions=5, provider="both"):

    token = gen_session_token()

    game_questions = {}

    for round in range(1, rounds+1):
        
        game_questions[str(round)] = {}

        for question in range(1, num_questions+1):

            if round == 1:
                game_questions[str(round)][f"{round}_{question}"] = random_question("easy", provider, token)
            elif round == rounds:
                game_questions[str(round)][f"{round}_{question}"] = random_question("hard", provider, token)
            elif 0.33 < (round/rounds) <= 0.67:
                game_questions[str(round)][f"{round}_{question}"] = random_question("medium", provider, token)

                    
            else:

                if round/rounds <= 0.33:

                    if random.random() >= (round/rounds):
                        game_questions[str(round)][f"{round}_{question}"] = random_question("easy", provider, token)
                    else:
                        game_questions[str(round)][f"{round}_{question}"] = random_question("medium", provider, token)

                elif round/rounds > 0.66:

                    if random.random() <= (round/rounds):
                        game_questions[str(round)][f"{round}_{question}"] = random_question("hard", provider, token)
                    else:
                        game_questions[str(round)][f"{round}_{question}"] = random_question("medium", provider, token)

            # print(f"{round}-{question} gen")

            if question == (num_questions):
                game_questions[str(round)][f"{round}_{question}"]['bonus'] = True
            else:
                game_questions[str(round)][f"{round}_{question}"]['bonus'] = False


    game_questions[str(round)][f"{rounds}_{num_questions-1}"] = random_question("easy", provider, token)
    game_questions[str(round)][f"{rounds}_{num_questions-1}"] ['bonus'] = False

    return game_questions



def generate_round(round, rounds=4, num_questions=5, provider="both"):

    token = gen_session_token()

    game_questions = {}


    for question in range(1, num_questions+1):

        if round == 1:
            game_questions[f"{round}_{question}"] = random_question("easy", provider, token)
        elif round == rounds:
            game_questions[f"{round}_{question}"] = random_question("hard", provider, token)
        elif 0.33 < (round/rounds) <= 0.66:
            game_questions[f"{round}_{question}"] = random_question("medium", provider, token)
        
        else:

            if round/rounds <= 0.33:

                if random.random() >= (round/rounds):
                    game_questions[f"{round}_{question}"] = random_question("easy", provider, token)
                else:
                    game_questions[f"{round}_{question}"] = random_question("medium", provider, token)

            elif round/rounds > 0.66:

                if random.random() >= (round/rounds):
                    game_questions[f"{round}_{question}"] = random_question("hard", provider, token)
                else:
                    game_questions[f"{round}_{question}"] = random_question("medium", provider, token)


    game_questions[f"{rounds}_{num_questions-1}"] = random_question("easy", provider, token)

    return game_questions





                