/**
 * Proxy to use both WebSocket and XMLHttpResquest in
 * the same way
 */

var ServerName = 'localhost:8888';

var ServerComm = Class.extend({
    init: function() {
        //this.use = ServerComm.XMLHttp;
        this.server = (this.use === ServerComm.XMLHttp ? 'http://' : 'ws://') + ServerName;
        this.use = window.WebSocket ? ServerComm.WebSock : ServerComm.XMLHttp;

        if (this.use == ServerComm.WebSock) {
            this.sock = new WebSocket(this.server + '/ws/');
            console.log('Using websocket');
        } else {

            this.sock = new XMLHttpRequest();
            this.sock.addEventListener('load', this.onXMLComplete.bind(this));
            this.sock.addEventListener('error', this.onXMLError.bind(this));
        }
    },

    done: function() {
        delete this.sock;
    },

    send: function(path, value) {
        alert(this.use);
        if (this.use == ServerComm.XMLHttp) {
            alert(path);
            this.sock.open('get', this.server + path + '?email=' + value);
            this.sock.send();
        } else {

        }
    },

    onXMLComplete: function(evt) {
        if (evt.currentTarget.readyState === 4) {
            if (evt.currentTarget.status === 200) {
                var json = JSON.parse(evt.currentTarget.responseText);
                if (json.success && json.success === true) {
                    this.emit(ServerComm.Signals.Complete, JSON.parse(evt.currentTarget.responseText));
                    return;
                }
            }
        }
        this.onXMLError(evt);
    },

    onXMLError: function(evt) {

    }
});

ServerComm.XMLHttp = 0;
ServerComm.WebSock = 1;

ServerComm.Signals = {
    Complete: 'servercomm.complete',
    Error: 'servercomm.error'
};
