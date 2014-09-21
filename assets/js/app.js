// Generated by CoffeeScript 1.7.1
(function() {
  var BaseModel, ContactMessage, Dialog, Model, RegexList, SaveDialog, YesNoDialog, cApplication, cMessageDialog, cModelAjax, cModelSocket, cObject, cOptionDialog, cOptionDialogModel, cUIView,
    __hasProp = {}.hasOwnProperty,
    __extends = function(child, parent) { for (var key in parent) { if (__hasProp.call(parent, key)) child[key] = parent[key]; } function ctor() { this.constructor = child; } ctor.prototype = parent.prototype; child.prototype = new ctor(); child.__super__ = parent.prototype; return child; },
    __bind = function(fn, me){ return function(){ return fn.apply(me, arguments); }; };

  $(function() {
    return $("[data-delete-confirm]").on('click', function() {
      var aElement, data;
      data = $(this).data('rel');
      aElement = $("[data-dialog-url]");
      return aElement.attr('href', (aElement.attr('href')) + data + '/');
    });
  });

  cApplication = (function() {
    function cApplication() {
      var el, message, _i, _len;
      this.currentSave = null;
      this.view = new cUIView;
      this.optionsDialog = new cOptionDialog;
      this.contactDialog = new ContactMessage();
      this.model = window.WebSocket ? new cModelSocket : new cModelAjax;
      this.model.connect(Model.Signals.SendError, (function(_this) {
        return function(msg) {
          new cMessageDialog("Error", "Unable to connect the server " + msg);
        };
      })(this)).connect(Model.Signals.SendSuccess, (function(_this) {
        return function(data) {
          if (!data.success) {
            new cMessageDialog("Error", data.error);
          } else {
            $("#dest_result").html("<pre><code>" + data.content + "</code></pre>");
          }
        };
      })(this)).connect(Model.Signals.SaveSuccess, (function(_this) {
        return function(data) {
          _this.saveDialog.close();
          if (!data.success) {
            new cMessageDialog("Error", data.error);
          } else {
            _this.view.displaySuccessMessage("Regular expression saved with success");
            _this.currentSave = data.name;
          }
        };
      })(this)).connect(Model.Signals.SaveError, (function(_this) {
        return function(data) {
          new cMessageDialog("Error", data);
        };
      })(this));
      if (document.location.pathname === '/') {
        window.onunload = (function(_this) {
          return function(e) {
            return _this.model.saveTempRegex();
          };
        })(this);
        this.model.restoreTempRegex();
        this.saveDialog = new SaveDialog();
        this.saveDialog.connect(Dialog.Signals.Open, (function(_this) {
          return function() {
            return _this.saveDialog.setName(_this.model.getRegexName());
          };
        })(this));
        this.saveDialog.connect(Dialog.Signals.SaveSuccess, (function(_this) {
          return function(name) {
            var regex;
            regex = $("#src_regex").val();
            return _this.model.saveRegex(name, regex);
          };
        })(this));
        $("#src_evaluate").on('click', this.evaluate.bind(this));
        document.getElementById('regex-name').textContent = this.model.getRegexName();
      }
      for (_i = 0, _len = messages.length; _i < _len; _i++) {
        message = messages[_i];
        $.UIkit.notify({
          message: message.message,
          status: !message.level ? 'success' : 'danger',
          pos: 'top-center',
          timeout: 3000
        });
      }
      if (document.location.pathname.indexOf("/user/regex/" !== -1)) {
        this.regexList = new RegexList({
          "delete": (function(_this) {
            return function(id, cb) {
              _this.model.deleteRegex(id, cb);
            };
          })(this),
          use: (function(_this) {
            return function(regex, name) {
              _this.model.setTempRegex(regex);
              _this.model.setRegexName(name);
              document.location = '/';
            };
          })(this)
        });
      }
      el = document.getElementById('clear-data');
      if (el) {
        el.onclick = (function(_this) {
          return function(e) {
            var src;
            e.preventDefault();
            _this.model.clearLocal();
            src = document.getElementById('src_regex');
            if (src) {
              src.value = '';
              document.getElementById('sourcetext').value = '';
            }
            return document.location = '/';
          };
        })(this);
      }
      return;
    }

    cApplication.prototype.getModel = function() {
      return this.model;
    };

    cApplication.prototype.evaluate = function() {
      var check, content, count, method, options, regex, sub, _i, _len, _ref;
      regex = $.trim($("#src_regex").val());
      content = $.trim($("#sourcetext").val());
      method = $("input[name=regex]:checked").val();
      options = [];
      if ($("#displaycommand").is("checked")) {
        options.push("displaycommand");
      }
      _ref = $("input[type=checkbox]:checked", "#regex_flags");
      for (_i = 0, _len = _ref.length; _i < _len; _i++) {
        check = _ref[_i];
        options.push($(check).data('name'));
      }
      if (!regex.length) {
        new cMessageDialog('Error', 'No regular expression entered');
      } else if (!content.length) {
        new cMessageDialog('Error', "You must enter some text to evaluate");
      } else {
        sub = count = void 0;
        if ($("#sub").is(':checked')) {
          sub = $("input[name=replacement]").val();
        } else if ($("#subn").is(':checked')) {
          count = parseInt($("input[name=maxreplacement]").val());
          sub = $("input[name=subnreplacement]").val();
        } else if ($("#split").is(':checked')) {
          count = $("#maxsplit").is(':checked');
        }
        this.model.sendRegex(regex, content, method, options, sub, count);
      }
      return this;
    };

    return cApplication;

  })();

  $(function() {
    var app;
    $("#main").css("min-height", $(document).height() - $("footer#footer").height() - 70);
    app = new cApplication();
  });


  /*
  Signal/Slot object
   */

  cObject = (function() {
    function cObject() {
      this.sig = [];
    }

    cObject.prototype.connect = function(signal, slot) {
      if (signal && slot) {
        this.sig.push({
          signal: signal,
          slot: slot
        });
      }
      return this;
    };

    cObject.prototype.emit = function(signal, args) {
      var ss, _i, _len, _ref;
      _ref = this.sig;
      for (_i = 0, _len = _ref.length; _i < _len; _i++) {
        ss = _ref[_i];
        if (ss.signal === signal) {
          ss.slot(args);
        }
      }
      return this;
    };

    return cObject;

  })();

  BaseModel = (function(_super) {
    __extends(BaseModel, _super);

    function BaseModel() {
      return BaseModel.__super__.constructor.apply(this, arguments);
    }

    BaseModel.prototype.sendRegex = function(regex, content, method, options, sub, count) {
      throw "saveRegex is not implemented";
    };

    BaseModel.prototype.saveRegex = function(name, regex) {
      return this.setRegexName(name);
    };

    BaseModel.prototype.deleteRegex = function(id) {
      throw "deleteRegex is not implementated";
    };

    BaseModel.prototype.saveTempRegex = function() {
      window.localStorage.setItem('regex', document.getElementById("src_regex").value || '');
      window.localStorage.setItem('sourcetext', document.getElementById("sourcetext").value || '');
    };

    BaseModel.prototype.setTempRegex = function(regex) {
      window.localStorage.setItem('regex', regex);
    };

    BaseModel.prototype.restoreTempRegex = function() {
      $("#src_regex").val((window.localStorage.getItem('regex')) || '');
      $("#sourcetext").val((window.localStorage.getItem('sourcetext')) || '');
    };

    BaseModel.prototype.setRegexName = function(name) {
      return window.localStorage.setItem('regexname', name);
    };

    BaseModel.prototype.getRegexName = function() {
      var name;
      name = window.localStorage.getItem('regexname');
      console.log(name);
      if (name === null || name === void 0) {
        return 'Untitled';
      }
      return name;
    };

    BaseModel.prototype.clearLocal = function() {
      window.localStorage.removeItem('regex');
      window.localStorage.removeItem('sourcetext');
      return window.localStorage.removeItem('regexname');
    };

    return BaseModel;

  })(cObject);

  ContactMessage = (function() {
    function ContactMessage() {
      this.validateForm = __bind(this.validateForm, this);
      var dialog;
      dialog = $("#contact");
      this.emailField = dialog.find("input[name=email]");
      this.nameField = dialog.find("input[name=name]");
      this.answerField = dialog.find("input[name=question]");
      this.messageField = dialog.find("textarea[name=message]");
      dialog.on('uk.modal.show', (function(_this) {
        return function() {
          _this.emailField.val("");
          _this.emailField.removeClass("uk-form-danger");
          _this.nameField.val("");
          _this.nameField.removeClass("uk-form-danger");
          _this.answerField.val("");
          _this.answerField.removeClass("uk-form-danger");
          _this.messageField.val("");
          return _this.messageField.removeClass("uk-form-danger");
        };
      })(this));
      dialog.find("[data-send]").on('click', this.validateForm);
    }

    ContactMessage.prototype.validateForm = function(e) {
      var error, formData, jqxhr;
      error = [];
      if ($.trim(this.emailField.val()).length === 0) {
        this.emailField.addClass("uk-form-danger");
        error.push("The email is empty");
      } else {
        this.emailField.removeClass("uk-form-danger");
      }
      if ($.trim(this.nameField.val()).length === 0) {
        this.nameField.addClass("uk-form-danger");
        error.push("The name is empty");
      } else {
        this.nameField.removeClass("uk-form-danger");
      }
      if ($.trim(this.answerField.val()).length === 0) {
        this.answerField.addClass("uk-form-danger");
        error.push("The answer is empty");
      } else if (this.answerField.val() !== $("#result").val()) {
        this.answerField.addClass("uk-form-danger");
        error.push("This isn't the good answer");
      } else {
        this.answerField.removeClass("uk-form-danger");
      }
      if ($.trim(this.messageField.val()).length === 0) {
        this.messageField.addClass("uk-form-danger");
        error.push("The message is empty");
      } else {
        this.messageField.removeClass("uk-form-danger");
      }
      if (error.length) {
        e.preventDefault();
        alert("There is one or more error\n\n" + error.join("\n"));
        return;
      }
      formData = new FormData(document.getElementById("contactform"));
      $("#form-container").slideUp('fast', (function(_this) {
        return function() {
          $("#wheel-container").removeClass('uk-hidden');
          return _this.addClass('uk-hidden');
        };
      })(this));
      jqxhr = $.ajax({
        url: '/contact',
        type: 'POST',
        data: formData,
        processData: false,
        contentType: false
      });
      jqxhr.always(function(data) {
        $("#wheel-container").addClass('uk-hidden');
        return $("#form-container").removeClass('uk-hidden');
      });
      jqxhr.done(function(data) {
        var errorModal, okModal;
        if (!data.match(/^error/)) {
          okModal = new $.UIkit.modal.Modal("#send-success");
          return okModal.show();
        } else {
          errorModal = new $.UIkit.modal.Modal("#connection-error");
          document.getElementById("connection-error-msg").innerHTML = data;
          return errorModal.show();
        }
      });
      jqxhr.fail(function(xhr) {
        var errorModal;
        errorModal = new $.UIkit.modal.Modal("#connection-error");
        document.getElementById("connection-error-msg").innerHTML = xhr.responseText;
        return errorModal.show();
      });
    };

    return ContactMessage;

  })();

  cMessageDialog = (function() {
    function cMessageDialog(title, msg) {
      $("#messagedialog").find('[data-content]').html(msg);
      $("#messagedialog").find('[data-title]').html(title);
      new $.UIkit.modal("#messagedialog").show();
    }

    cMessageDialog.prototype.on = function(signal, func) {};

    return cMessageDialog;

  })();

  cModelAjax = (function(_super) {
    __extends(cModelAjax, _super);

    function cModelAjax() {
      cModelAjax.__super__.constructor.call(this);
    }

    cModelAjax.prototype.sendRegex = function(regex, content, method, options, sub, count) {
      var data;
      data = {
        regex: regex,
        content: content,
        method: method,
        options: options,
        sub: sub || null,
        count: count || null
      };
      return $.getJSON('/wsa/', {
        json: JSON.stringify(data)
      }).fail((function(_this) {
        return function(xhr) {
          return _this.emit(Model.Signals.SendError, xhr.responseText);
        };
      })(this)).done((function(_this) {
        return function(data) {
          return _this.emit(Model.Signals.SendSuccess, data);
        };
      })(this));
    };

    cModelAjax.prototype.saveRegex = function(name, regex) {
      cModelAjax.__super__.saveRegex.call(this);
      alert(name);
      return alert(regex);
    };

    cModelAjax.prototype.deleteRegex = function(id, cb) {
      return $.ajax('/user/regex/', {
        id: id,
        type: 'DELETE',
        dataType: 'application/json',
        error: function(xhr) {
          return alert("Error " + xhr.responseText);
        },
        success: function(data) {
          return cb(id);
        }
      });
    };

    return cModelAjax;

  })(BaseModel);

  cModelSocket = (function(_super) {
    __extends(cModelSocket, _super);

    function cModelSocket() {
      return cModelSocket.__super__.constructor.apply(this, arguments);
    }

    cModelSocket.prototype.send = function(data, successSignal, errorSignal) {
      var socket;
      socket = new WebSocket('ws://localhost:8888/ws/');
      socket.onmessage = (function(_this) {
        return function(e) {
          _this.emit(successSignal, JSON.parse(e.data));
        };
      })(this);
      socket.onerror = (function(_this) {
        return function(e) {
          _this.emit(errorSignal, e.data);
        };
      })(this);
      socket.onopen = (function(_this) {
        return function(e) {
          socket.send(JSON.stringify(data));
        };
      })(this);
    };

    cModelSocket.prototype.sendRegex = function(regex, content, method, options, sub, count) {
      var data;
      data = {
        action: 'evaluate',
        regex: regex,
        content: content,
        method: method,
        options: options,
        flags: options,
        sub: sub || null,
        count: count || null
      };
      return this.send(data, Model.Signals.SendSuccess, Model.Signals.SendError);
    };

    cModelSocket.prototype.saveRegex = function(name, regex) {
      var data;
      cModelSocket.__super__.saveRegex.call(this);
      data = {
        action: 'save',
        name: name,
        regex: regex
      };
      return this.send(data, Model.Signals.SaveSuccess, Model.Signals.SaveError);
    };

    cModelSocket.prototype.deleteRegex = function(id, cb) {
      var data;
      data = {
        action: "delete",
        id: id
      };
      this.connect(Model.Signals.DeleteRegexSuccess, (function(_this) {
        return function() {
          if (typeof cb === 'function') {
            return cb(id);
          }
        };
      })(this));
      return this.send(data, Model.Signals.DeleteRegexSuccess, Model.Signals.DeleteRegexError);
    };

    return cModelSocket;

  })(BaseModel);


  /*
  OptionDialogModel - Manage persistant options
   */

  cOptionDialogModel = (function() {
    function cOptionDialogModel() {
      var ls;
      this.evaluateOnChange = false;
      this.liveEvaluation = false;
      this.shortTag = false;
      this.tags = {
        debug: false,
        ignoreCase: false,
        multiline: false,
        dotAll: false,
        unicode: false,
        verbose: false
      };
      if (window.localStorage) {
        ls = window.localStorage;
        this.evaluateOnChange = ls.getItem('opt_change' === '1');
        this.liveEvaluation = ls.getItem('opt_typing' === '1');
        this.shortTag = ls.getItem('opt_short' === '1');
        this.tags.debug = ls.getItem('re_debug' === '1');
        this.tags.ignoreCase = ls.getItem('re_ignore' === '1');
        this.tags.multiline = ls.getItem('re_multiline' === '1');
        this.tags.dotAll = ls.getItem('re_dotall' === '1');
        this.tags.unicode = ls.getItem('re_unicode' === '1');
        this.tags.verbose = ls.getItem('re_verbose' === '1');
      }
    }

    cOptionDialogModel.prototype.change = function() {
      var ls;
      this.evaluateOnChange = $("#opt_change").is(':checked');
      this.liveEvaluation = $("#opt_typing").is(':checked');
      this.shortTag = $("#opt_short").is(':checked');
      this.tags.debug = $("#re_debug").is(':checked');
      this.tags.ignoreCase = $("#re_ignore").is(':checked');
      this.tags.multiline = $("#re_multiline").is(':checked');
      this.tags.dotAll = $("#re_dotall").is(':checked');
      this.tags.unicode = $("#re_unicode").is(':checked');
      this.tags.verbose = $("#re_verbose").is(':checked');
      if (window.localStorage) {
        ls = window.localStorage;
        ls.setItem('opt_change', this.evaluateOnChange === true ? '1' : '0');
        ls.setItem('opt_typing', this.liveEvaluation === true ? '1' : '0');
        ls.setItem('opt_short', this.shortTag === true ? '1' : '0');
        ls.setItem('re_debug', this.tags.debug === true ? '1' : '0');
        ls.setItem('re_ignore', this.tags.ignoreCase === true ? '1' : '0');
        ls.setItem('re_multiline', this.tags.multiline === true ? '1' : '0');
        ls.setItem('re_dotall', this.tags.dotAll === true ? '1' : '0');
        ls.setItem('re_unicode', this.tags.unicode === true ? '1' : '0');
        return ls.setItem('re_verbose', this.tags.verbose === true ? '1' : '0');
      }
    };

    return cOptionDialogModel;

  })();


  /*
  OptionDialog - Manage UIKit dialog box
   */

  cOptionDialog = (function() {
    function cOptionDialog() {
      this.model = new cOptionDialogModel;
      $("#options").on('click', '[data-ok]', this.model.change.bind(this.model));
      $("#options").on('uk-model-show', this.onOpen.bind(this));
    }

    cOptionDialog.prototype.onOpen = function() {
      $("#opt_change").attr('checked', this.model.evaluateOnChange);
      $("#opt_typing").attr('checked', this.model.liveEvaluation);
      $("#opt_short").attr('checked', this.model.shortTag);
      $("#re_debug").attr('checked', this.model.tags.debug);
      $("#re_ignore").attr('checked', this.model.tags.ignoreCase);
      $("#re_multiline").attr('checked', this.model.tags.multiline);
      $("#re_dotall").attr('checked', this.model.tags.dotAll);
      $("#re_unicode").attr('checked', this.model.tags.unicode);
      return $("#re_verbose").attr('checked', this.model.tags.verbose);
    };

    return cOptionDialog;

  })();

  RegexList = (function() {
    function RegexList(args) {
      this.useRegex = $("#use-regex");
      this.md = null;
      $("[data-delete-regex]").on('click', (function(_this) {
        return function(evt) {
          evt.preventDefault();
          if (_this.md === null) {
            _this.md = new YesNoDialog("Delete regex", "Are you sure you want to delete this regular expression?");
          }
          _this.md.on("yes", function(e) {
            var id;
            id = evt.target.getAttribute('data-id');
            return args["delete"](id, function() {
              var el;
              el = document.querySelector('tr[data-id="' + evt.target.getAttribute('data-id') + '"]');
              return el.parentNode.removeChild(el);
            });
          });
          return _this.md.show();
        };
      })(this));
      $("[data-use-regex]").on('click', (function(_this) {
        return function(e) {
          var selector;
          e.preventDefault();
          selector = document.querySelector('tr[data-id="' + e.target.getAttribute('data-id') + '"]');
          return args.use(selector.querySelector('[data-regex-content]').textContent, e.target.getAttribute('data-name'));
        };
      })(this));
      return;
    }

    return RegexList;

  })();

  SaveDialog = (function(_super) {
    __extends(SaveDialog, _super);

    function SaveDialog() {
      this.setName = __bind(this.setName, this);
      SaveDialog.__super__.constructor.call(this);
      this.saveDialog = $("#savedialog");
      this.saveDialog.find("button#save").on('click', this.onSave.bind(this));
      this.inputName = this.saveDialog.find('input[name=name]');
      this.saveDialog.on('uk.modal.show', (function(_this) {
        return function() {
          _this.inputName.val('');
          _this.emit(Dialog.Signals.Open);
          _this.inputName.focus();
          _this.saveDialog.find('i.uk-icon-spin').addClass('uk-hidden');
          _this.saveDialog.find('i.uk-icon-times').removeClass('uk-hidden');
        };
      })(this));
    }

    SaveDialog.prototype.onSave = function() {
      var name;
      name = $.trim(this.inputName.val());
      if (name === '') {
        return;
      }
      this.saveDialog.find('i').toggleClass('uk-hidden');
      this.emit(Dialog.Signals.SaveSuccess, name);
    };

    SaveDialog.prototype.close = function() {
      return ($.UIkit.modal(this.saveDialog)).hide();
    };

    SaveDialog.prototype.setName = function(name) {
      if (typeof name === 'string') {
        return this.inputName.val(name);
      }
    };

    return SaveDialog;

  })(cObject);


  /*
  This simply put in a namespace the model signals
   */

  Model = {
    Signals: {
      SendSuccess: 'model.regex.success',
      SendError: 'model.regex.error',
      SocketClosed: 'model.socket.closed',
      SaveSuccess: 'model.save.success',
      SaveError: 'model.save.error',
      DeleteRegexSuccess: 'model.delete.success',
      DeleteRegexError: 'model.delete.error'
    }
  };

  Dialog = {
    Signals: {
      Open: 'dialog.regex.open',
      SaveSuccess: 'dialog.regex.save.success',
      SaveError: 'dialog.regex.save.error'
    }
  };


  /*
  Class UIView
  This class handle all views on the screen.
  There's only one view because there isn't a lot of UIs
   */

  cUIView = (function() {
    function cUIView() {
      this.slideDown = true;
      this.storejQueryObjects();
      this.forceCheck();
      this.prepareUI();
      this.connectUI();
    }

    cUIView.prototype.forceCheck = function() {
      var checked, _i, _len, _ref, _results;
      _ref = $("input[type=radio]:checked");
      _results = [];
      for (_i = 0, _len = _ref.length; _i < _len; _i++) {
        checked = _ref[_i];
        switch (checked.getAttribute('id')) {
          case 'split':
            _results.push(this.displaySplitOptions());
            break;
          case 'sub':
            _results.push(this.displaySubOptions());
            break;
          case 'subn':
            _results.push(this.displaySubnOptions());
            break;
          case 'displaycommand':
            _results.push(this.displayCommandLine());
            break;
          default:
            _results.push(void 0);
        }
      }
      return _results;
    };

    cUIView.prototype.storejQueryObjects = function() {
      this.splitOptions = $("#splitoptions");
      this.subnOptions = $("#subnoptions");
      this.subOptions = $("#suboptions");
      this.inputRadioSplit = $("input#split");
      this.inputRadioSub = $("input#sub");
      this.inputRadioSubn = $("input#subn");
      this.inputFieldReplacement = $("input[name=replacement]");
      this.inputFieldSubnreplacement = $("input[name=subnreplacement]");
      this.inputFieldMaxreplacement = $("input[name=maxreplacement]");
      return this.inputFieldMaxsplit = $("input[name=maxsplit]");
    };

    cUIView.prototype.prepareUI = function() {
      this.splitOptions.hide();
      this.subnOptions.hide();
      return this.subOptions.hide();
    };

    cUIView.prototype.connectUI = function() {
      $("input[type=radio]").on({
        'click': function(e) {
          return $("[data-option]").hide();
        }
      });
      this.inputRadioSplit.on('click', this.displaySplitOptions.bind(this));
      this.inputRadioSub.on('click', this.displaySubOptions.bind(this));
      this.inputRadioSubn.on('click', this.displaySubnOptions.bind(this));
      return $("input#displaycommand").on('click', this.displayCommandLine.bind(this));
    };

    cUIView.prototype.displaySplitOptions = function(e) {
      this.inputFieldMaxsplit.val(0);
      return this.splitOptions.show();
    };

    cUIView.prototype.displaySubOptions = function(e) {
      this.inputFieldReplacement.val('');
      return this.subOptions.show();
    };

    cUIView.prototype.displaySubnOptions = function(e) {
      this.inputFieldSubnreplacement.val('');
      this.inputFieldMaxreplacement.val(0);
      return this.subnOptions.show();
    };

    cUIView.prototype.displayCommandLine = function(e) {
      if ($("#dest_result").html() !== 'Not yet evaluated') {
        $("#src_evaluate").trigger('click');
      }
      return null;
    };

    cUIView.prototype.displaySuccessMessage = function(msg) {
      return $.UIkit.notify({
        message: msg,
        status: 'success',
        timeout: 5000,
        pos: 'top-center'
      });
    };

    return cUIView;

  })();

  YesNoDialog = (function() {
    function YesNoDialog(title, msg) {
      var dialog;
      dialog = document.querySelector("#yesnodialog");
      dialog.querySelector("[data-content]").innerHTML = msg;
      dialog.querySelector('[data-title]').innerHTML = title;
    }

    YesNoDialog.prototype.show = function() {
      return new $.UIkit.modal("#yesnodialog").show();
    };

    YesNoDialog.prototype.hide = function() {
      return $("#yesnodialog").hide();
    };

    YesNoDialog.prototype.on = function(signal, func) {
      document.querySelector("button#" + signal).onclick = func;
    };

    return YesNoDialog;

  })();

}).call(this);
