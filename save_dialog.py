def save_dialog(user, dialog):
    import pickle
    with open(f'C:/Program Files (x86)/Messenger/Dialogs/{user}', 'wb') as output:
        pickle.dump(dialog, output)

    with open(f'C:/Program Files (x86)/Messenger/Dialogs/{user}', 'rb') as input:
        dialog = pickle.load(input)
        print(dialog)
