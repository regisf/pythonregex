var UIView = Class.extend({
    init: function() {
        // Ensure the footer in on the bottom of the window
        $("#main").css('min-height', ($(document).height() - $("footer#footer").height() - 70));

        // Store HTML element. Avoid jQuery search each time
        // Milliseconds after milliseconds the app is doing its
        // job faster
        this.slideDown = true;
        this.splitoptions = $("#splitoptions");
        this.subnoptions = $("#subnoptions");
        this.suboptions = $("#suboptions");
        this.input = {
            radio: {
                split:$("input#split"),
                sub:$("input#sub"),
                subn:$("input#subn")
            },
            fields: {
                replacement: $("input[name=replacement]"),
                subnreplacement: $("input[name=subnreplacement]"),
                maxreplacement:$("input[name=maxreplacement]"),
                maxsplit: $("input[name=maxsplit]")
            },
        };

        this.splitoptions.hide();
        this.subnoptions.hide();
        this.suboptions.hide();

        // Force check on reload
        var checked = $("input[type=radio]:checked");
        for(var i=0; i < checked.length; i++) {
            switch (checked[i].getAttribute('id')) {
                case 'split':
                    this.displaySplitOptions();
                    break;

                case 'sub':
                    this.displaySubOptions();
                    break;

                case 'subn':
                    this.displaySubnOptions();
                    break;

                case 'displaycommand':
                    this.displayCommandLine();
                    break;
            }
        }

        $('input[type=radio]').on('click', function() {
            $("[data-option]").hide();
        });

        this.input.radio.split
            .on('click', this.displaySplitOptions.bind(this));

        this.input.radio.sub
            .on('click', this.displaySubOptions.bind(this));
        this.input.radio.subn
            .on('click', this.displaySubnOptions.bind(this));

        $("input#displaycommand")
            .on('click', this.displayCommandLine.bind(this));
    },

    /**
     * Display the split field
     */
    displaySplitOptions: function() {
        this.input.fields.maxsplit.val(0);
        this.splitoptions.show();
    },

    displaySubOptions: function() {
        this.input.fields.replacement.val('');
        this.suboptions.show();
    },

    displaySubnOptions: function() {
        this.input.fields.subnreplacement.val('');
        this.input.fields.maxreplacement.val(0);
        this.subnoptions.show();
    },

    displayCommandLine: function() {
        if ($("#dest_result").html() != 'No yet evaluated') {
            $("#src_evaluate").trigger('click');
        }
    },

});
