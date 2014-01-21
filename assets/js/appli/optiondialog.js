/**
 * Controller for the options dialog
 */
var OptionDialog = Class.extend({
    /** Pseudo constructor */
    init: function() {
        var self=this;
        this.model = new OptionDialog.Model();

        $("#options").on('click', '[data-ok]', this.model.change.bind(this.model));
        $("#options").on('uk.modal.show', this.onOpen.bind(this));
    },

    /**
     * Call the dialog is opened
     * @param {Object} The jQuery event
     */
    onOpen: function(evt) {
        $("#opt_change").attr('checked', this.model.evaluateOnChange);
        $("#opt_typing").attr('checked', this.model.liveEvaluation);
        $("#opt_short").attr('checked', this.model.shortTag);
        $("#re_debug").attr('checked', this.model.tags.debug);
        $("#re_ignore").attr('checked', this.model.tags.ignoreCase);
        $("#re_multiline").attr('checked', this.model.tags.multiline);
        $("#re_dotall").attr('checked', this.model.tags.dotAll);
        $("#re_unicode").attr('checked', this.model.tags.unicode);
        $("#re_verbose").attr('checked', this.model.tags.verbose);
    }
});

/**
 * Store the options
 */
OptionDialog.Model = Class.extend({
    /**
     * Pseudo constructor
     * Set options to default
     */
    init: function() {
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

        this._retreive();
    },

    /**
     * Callback for OK button pressed. Store in memory
     * @see OptionDialog
     */
    change: function() {
        this.evaluateOnChange = $("#opt_change").is(':checked');
        this.liveEvaluation =   $("#opt_typing").is(':checked');
        this.shortTag =         $("#opt_short").is(':checked');
        this.tags.debug =       $("#re_debug").is(':checked');
        this.tags.ignoreCase =  $("#re_ignore").is(':checked');
        this.tags.multiline =   $("#re_multiline").is(':checked');
        this.tags.dotAll =      $("#re_dotall").is(':checked');
        this.tags.unicode =     $("#re_unicode").is(':checked');
        this.tags.verbose =     $("#re_verbose").is(':checked');
        this._store();
    },

    /**
     * Private. Store options using HTML5 localStorage
     * A developper shall not use a antique browser (no polyfill)
     */
    _store: function() {
        if (window.localStorage) {
            localStorage.setItem('opt_change',  this.evaluateOnChange === true ? '1' : '0');
            localStorage.setItem('opt_typing',  this.liveEvaluation === true ? '1' : '0');
            localStorage.setItem('opt_short',   this.shortTag === true ? '1' : '0');
            localStorage.setItem('re_debug',    this.tags.debug === true ? '1' : '0');
            localStorage.setItem('re_ignore',   this.tags.ignoreCase === true ? '1' : '0');
            localStorage.setItem('re_multiline',this.tags.multiline === true ? '1' : '0');
            localStorage.setItem('re_dotall',   this.tags.dotAll === true ? '1' : '0');
            localStorage.setItem('re_unicode',  this.tags.unicode === true ? '1' : '0');
            localStorage.setItem('re_verbose',  this.tags.verbose === true ? '1' : '0');
        }
    },

    /**
     * Private. Try to retreive options usings HTML5 localStorage
     * A developper shall not use a antique browser (no polyfill)
     */
    _retreive: function() {
        if (window.localStorage) {
            this.evaluateOnChange = localStorage.getItem('opt_change') === '1';
            this.liveEvaluation = localStorage.getItem('opt_typing') === '1';
            this.shortTag = localStorage.getItem('opt_short') === '1';
            this.tags.debug = localStorage.getItem('re_debug') === '1';
            this.tags.ignoreCase = localStorage.getItem('re_ignore') === '1';
            this.tags.multiline = localStorage.getItem('re_multiline') === '1';
            this.tags.dotAll = localStorage.getItem('re_dotall') === '1';
            this.tags.unicode = localStorage.getItem('re_unicode') === '1';
            this.tags.verbose = localStorage.getItem('re_verbose') === '1';
        }
    }
});
