#_require cobject
class cModelSocket extends cObject
    constructor: ->
        super()


    sendRegex: (regex, content, method, options, sub, count) ->
        data =
            regex: regex
            content: content
            method: method
            options: options
            flags: options
            sub: sub or null
            count: count or null

        socket = new WebSocket('ws://localhost:8888/ws/')

        socket.onmessage = (e) =>
            @emit Model.Signals.SendSuccess, JSON.parse e.data

        socket.onerror = (e) =>
            @emit Model.Signals.SendError, e

        socket.onopen = (e) =>
            socket.send JSON.stringify data
