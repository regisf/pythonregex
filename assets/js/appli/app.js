
function Application() {
    return new Application.controller();
};


Application.controller = Class.extend({
    init: function() {
        this.uiView = new UIView();
        this.optionDialog = new OptionDialog();

        $("#src_evaluate").bind('click', this.onEvaluate.bind(this));

        this.model = window.WebSocket ? new ModelSocket() : new ModelAjax();

        this.model
            .connect(Model.Signals.SendError, this.onSendError.bind(this))
            .connect(Model.Signals.SendSuccess, this.onSendSuccess.bind(this))
            .connect(Model.Signals.SocketClosed, this.onSocketClosed.bind(this));

        //$("#regex_flags input[type=checkbox]").bind('click', function() { alert("ok")});

    },

    onEvaluate: function(e) {
        var regex = $.trim($("textarea#src_regex").val()),
            content = $.trim($("textarea#sourcetext").val()),
            method = $("input[name=regex]:checked").val(),
            options = [];

        $("input#displaycommand").is(':checked') ? options.push('displaycommand') : '';
        checked = $("input[type=checkbox]:checked", "#regex_flags");

        $.each(checked, function(a,b) {
            options.push($(this).data('name'));
        });

        if (regex == '') {
            new MessageDialog('Error', 'No regular expression entered');
            return;
        }

        if (content == '') {
            new MessageDialog("Error", "You must enter some text to evaluate");
            return;
        }

        var sub = null, count = null;
        if ($("input#sub").is(':checked')) {
            sub = $("input[name=replacement]").val();
        } else if ($("input#subn").is(':checked')) {
            sub = $("input[name=subnreplacement]").val();
            count = parseInt($("input[name=maxreplacement]").val());
        } else if ($("input#split").is(':checked')) {
            count = $("input[name=maxsplit]").val();
        }
        this.model.sendRegex(regex, content, method, options, sub, count);
    },

    onSendSuccess: function(data) {
        if (data.success == false) {
            new MessageDialog("ERROR",data.error);
            return;
        }
        $("#dest_result").html('<pre><code>' + data.content + '</code></pre>')
    },

    onSendError: function(msg) {
        new MessageDialog("Error", "Unable to connect to the server: "+msg);
    },

    onSocketClosed: function(obj) {
        new MessageDialog("Caution", "The server closed the socket.");
    }
});

/**
 * Main application entry point
 */
$(document).ready(function() {
    var app = Application();
});
