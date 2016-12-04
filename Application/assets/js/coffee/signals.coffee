###
This simply put in a namespace the model signals
###
Model =
    Signals:
        SendSuccess: 'model.regex.success'
        SendError: 'model.regex.error'
        SocketClosed: 'model.socket.closed'
        SaveSuccess: 'model.save.success'
        SaveError: 'model.save.error'
        DeleteRegexSuccess: 'model.delete.success'
        DeleteRegexError: 'model.delete.error'

Dialog =
    Signals:
        Open: 'dialog.regex.open'
        SaveSuccess: 'dialog.regex.save.success'
        SaveError: 'dialog.regex.save.error'
