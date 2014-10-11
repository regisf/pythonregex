#_require basemodel

class cModelSocket extends BaseModel
    canDoWebSocket: (cb) ->
        try
            socket = new WebSocket('ws:/python-regex.com/ws/')
#            socket = new WebSocket('ws:/localhost:888/ws/')
            socket.onerror = (e) =>
                console.log 'I cant do it'
                cb false
                return

            socket.onopen = (e) =>
                console.log "I can do it"
                cb true
                return
        catch e
            console.log "i can't do it"
            cb false
            return

    send: (data, successSignal, errorSignal) ->
#        socket = new WebSocket('ws://localhost:8888/ws/')
        socket = new WebSocket('ws://python-regex.com/ws/')

        socket.onmessage = (e) =>
            @emit successSignal, JSON.parse e.data
            return

        socket.onerror = (e) =>
            @emit errorSignal, e.data
            return

        socket.onopen = (e) =>
            socket.send JSON.stringify data
            return
        return

    sendRegex: (regex, content, method, options, sub, count) ->
        data =
            action: 'evaluate'
            regex: regex
            content: content
            method: method
            options: options
            flags: options
            sub: sub or null
            count: count or null

        @send data, Model.Signals.SendSuccess, Model.Signals.SendError

    saveRegex: (name, regex) ->
        super()
        data =
            action: 'save'
            name: name
            regex: regex

        @send data, Model.Signals.SaveSuccess, Model.Signals.SaveError

    deleteRegex: (id, cb) ->
        data=
            action: "delete"
            id: id

        @connect Model.Signals.DeleteRegexSuccess, () =>
            if typeof cb == 'function'
                cb(id)

        @send data, Model.Signals.DeleteRegexSuccess, Model.Signals.DeleteRegexError
