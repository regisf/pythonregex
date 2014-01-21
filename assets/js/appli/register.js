function RegisterApp() {
    return new RegisterApp.Controller();
}

RegisterApp.Signals = {
    EmailChange: 'registerapp.view.emailChange',
    EmailFree: 'registerapp.model.emailfree',
    EmailExists: 'registerapp.model.emailexits'
};

RegisterApp.Controller = Class.extend({
    init: function() {
        this.model = new RegisterApp.Model();
        this.view = new RegisterApp.View();

        this.view.connect(RegisterApp.Signals.EmailChange, this.onEmailChange.bind(this));

        this.model
            .connect(RegisterApp.Signals.EmailExists, this.onEmailExists.bind(this))
            .connect(RegisterApp.Signals.EmailFree,   this.onEmailFree.bind(this));


    },

    onEmailChange: function(email) {
        this.view.displaySpinner("waitmail", true);
        this.model.isEmailExists(email);
    },

    onEmailExists: function() {
        this.view.displaySpinner('waitmail', false);
        this.view.setEmailError(true);
    },

    onEmailFree: function() {
        this.view.displaySpinner('waitmail', false);
        this.view.setEmailError(false);
    }
});

RegisterApp.Model = ServerComm.extend({
    init: function() {
        this.inherit();
        this
            .connect(ServerComm.Signals.Complete, this.onComplete.bind(this));
    },

    isEmailExists: function(email) {
        this.send('/auth/register/checkmailexists', email);
    },

    onComplete: function(jsonData) {
        switch (jsonData.action) {
            case 'checkmail':
                this.emit(jsonData.exists === false ?
                            RegisterApp.Signals.EmailFree :
                            RegisterApp.Signals.EmailExists);
                break;
        }
    }
});

RegisterApp.View = Class.extend({
    init: function() {
        var self=this;
        this.email = document.getElementsByName('email')[0];

        this.email.onchange = function() {
            self.emit(RegisterApp.Signals.EmailChange, this.value);
        }
    },

    displaySpinner: function(spinnerId, visible) {
        document.getElementById(spinnerId).style.display = visible === true  ? 'inline-block' : 'none';
    },

    setEmailError: function(err) {
        this.email.className += err === true ? ' uk-form-danger' : ' uk-form-success';
    }
});

$(document).ready(function() {
    var app = new RegisterApp();
});
