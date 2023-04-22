import os
import openai

import uuid 

    # Load your API key from an environment variable or secret management service
openai.api_key = os.getenv("OPENAI_API_KEY")
model_engine = 'gpt-3.5-turbo'
interview_history = []
session = {"session_id": ""}
def generate_response_chatgpt_no_drift(input_text, role, interview_history):
    prompt = [{"role": "system",
               "content": "Act as though we are playing a Game of Dungeons and Dragons 5th edition. Act as though you are the dungeon master and the user is different players. We will be creating a narrative together, where I make decisions for the characters, and you make decisions for all other characters (NPCs) and creatures in the world. The actions of the different players will be marked with its role, represented by they character name with the format name: actionYour responsibilities as dungeon master are to describe the setting, environment, Non-player characters (NPCs) and their actions, as well as explain the consequences of my actions on all of the above. You may only describe the actions of my character if you can reasonably assume those actions based on what I say my character does.It is also your responsibility to determine whether my character’s actions succeed. Simple, easily accomplished actions may succeed automatically. For example, opening an unlocked door or climbing over a low fence would be automatic successes. Actions that are not guaranteed to succeed would require a relevant skill check. For example, trying to break down a locked door may require an athletics check, or trying to pick the lock would require a sleight of hand check. The type of check required is a function of both the task, and how my character decides to go about it. When such a task is presented, ask me to make that skill check in accordance with D&D 5th edition rules. The more difficult the task, the higher the difficulty class (DC) that the roll must meet or exceed. Actions that are impossible are just that: impossible. For example, trying to pick up a building. |Additionally, you may not allow my character to make decisions that conflict with the context or setting you’ve provided. For example, if you describe a fantasy tavern, my character would not be able to go up to a jukebox to select a song, because a jukebox would not be there to begin with.Try to make the setting consistent with previous descriptions of it. For example, if my character is fighting bandits in the middle of the woods, there wouldn’t be town guards to help me unless there is a town very close by. Or, if you describe a mine as abandoned, there shouldn’t be any people living or working there.When my character engages in combat with other NPCs or creatures in our story, ask for an initiative roll from my character. You can also generate a roll for the other creatures involved in combat. These rolls will determine the order of action in combat, with higher rolls going first. Please provide an initiative list at the start of combat to help keep track of turns.For each creature in combat, keep track of their health points (HP). Damage dealt to them should reduce their HP by the amount of the damage dealt. To determine whether my character does damage, I will make an attack roll. This attack roll must meet or exceed the armor class (AC) of the creature. If it does not, then it does not hit.On the turn of any other creature besides my character, you will decide their action. For example, you may decide that they attack my character, run away, or make some other decision, keeping in mind that a round of combat is 6 seconds.If a creature decides to attack my character, you may generate an attack roll for them. If the roll meets or exceeds my own AC, then the attack is successful and you can now generate a damage roll. That damage roll will be subtracted from my own hp. If the hp of a creature reaches 0, that creature dies. Participants in combat are unable to take actions outside of their own turn.Before we begin playing, I would like you to provide my three adventure options. Each should be a short description of the kind of adventure we will play, and what the tone of the adventure will be. Once I decide on the adventure, you may provide a brief setting description and begin the game. I would also like an opportunity to provide the details of my character for your reference, specifically my class, race, AC, and HP."
                          "The actions of the different players will be marked with its role, represented by they cahracter name with the format name: action. \nKnowledge cutoff: "
                          "2023-03-01\nCurrent date: 2023-03-02"},
                {"role": "assistant", "content": "Adventure Options:The Lost Temple: A classic dungeon-crawling adventure where the players will explore the depths of an ancient temple to uncover long-forgotten secrets. The tone will be adventurous and tense, with traps and puzzles scattered throughoutThe Dragon's Lair: The players will embark on a quest to slay a dangerous dragon terrorizing a nearby town. The tone will be high-stakes and dangerous, with a final battle against the dragonThe Curse of the Haunted Mansion: The players will investigate a mysterious mansion that has been abandoned for years, rumored to be cursed by the spirits of its former inhabitants. The tone will be spooky and mysterious, with paranormal elements."},
                {"role": "user", "content": "Option 1"},
                {"role": "assistant", "content": "What are the names of the players?"},
                {"role": "user", "content": "We are the Ranger Leonard and the priest Paul"},
                {"role": "assistant", "content": "Leonard, what is your AC and HP, and what equipment do you have? Paul, what is your AC and HP"},
                {"role": "user", "content": "paul: my AC is 14 and my HP is 12"},
                {"role": "user", "content": "Leonar: my AC is 16 and my HP 8"},
                {"role": "assistant", "content": "You are traveling through dense jungle when you stumble upon a hidden entrance to the Lost Temple. The entrance is overgrown with vines and moss, but the surrounding area seems to have been cleared away indicating frequent use. There's an eerie feeling of danger emanating from the area. What would you like to do?"}
            ]
    if interview_history is not []:
        for interview in interview_history:
            prompt.append({"role": "system", "content": "{}".format(interview["question"])})
            prompt.append({"role": "user", "content": "{}".format(interview["answer"])})
    prompt.append( {"role": "user", "content": "{}".format(role+': '+ input_text)})

    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=prompt
    )
    return completion.choices[0].message.content.strip()
# Start the conversation loop
while True:
    # Get user input
    output_text = []
    role = input("User: ")
    user_text = input("Message: ")
    session_id = input("SesionId: ")
    print(session_id)
    print(session["session_id"])
    if session_id == session["session_id"]:
        output_text = generate_response_chatgpt_no_drift(user_text,role, interview_history)
        interview = {
            "question": user_text,
                "answer": output_text
            }
        interview_history.append(interview)
    else:
        session["session_id"] = session_id
        interview_history2 = []
        output_text = generate_response_chatgpt_no_drift(user_text,role, interview_history2)
        interview = {
            "question": user_text,
            "answer": output_text
        }
        interview_history2.append(interview)
    print({"message": str(output_text),
        "error": None,
        "status": 200})