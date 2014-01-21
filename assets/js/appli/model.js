var ModelAjax = Class.extend({
    sendRegex: function(regex, content, method, options, sub, count) {
        var self=this;
        d = {
            regex: regex,
            content:content,
            flags: options,
            method:method,
            options:options,
            sub: sub || null,
            count: count|| null
        }

        $.getJSON(ModelAjax.URL, { 'json': JSON.stringify(d)})
            .complete(function() { self.emit(Model.Signals.SendDone) })
            .error(function(xhr) { self.emit(Model.Signals.SendError, xhr.responseText) })
            .success(function(data) { self.emit(Model.Signals.SendSuccess, data)});
    }
});

ModelAjax.URL = '/wsa/'; //'http://localhost:8888/wsa/';
var Model = {
    Signals : {
        SendSuccess: 'model.send.success',
        SendDone : 'model.send.done',
        SendError: 'model.send.error',
        SocketClosed: 'model.socket.closed'
    }
};


var ModelSocket = Class.extend({
    init: function() {
        this.socket = new WebSocket("ws://localhost:8888/ws/");
        this.socket.onmessage = this.onResponse.bind(this);
        this.socket.onclose = this.onClose.bind(this);
    },

    sendRegex: function(regex, content, method, options, sub, count) {
        var self=this;
        d = {
            regex: regex,
            content:content,
            flags: options,
            method:method,
            options:options,
            sub: sub || null,
            count: count|| null
        }
        this.socket.send(JSON.stringify(d));
    },

    onResponse: function(e) {
        this.emit(Model.Signals.SendSuccess, JSON.parse(e.data));
    },

    /** The socket is closed by the server.
     * @param {Object} e The WebSocket event object
     */
    onClose: function(e) {
        this.emit(Model.Signals.SocketClosed, { sender:this, event: e});
    }
});
