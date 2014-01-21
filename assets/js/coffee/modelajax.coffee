#_require cobject

class cModelAjax extends cObject
    constructor: ->
        super()

    sendRegex: (regex, content, method, options, sub, count) ->
        data =
            regex: regex
            content: content
            method: method
            options: options
            sub: sub or null
            count: count or null

        $.getJSON '/wsa/', { json: JSON.stringify data }
            .fail (xhr) =>
                @emit Model.Signals.SendError, xhr.responseText

            .done (data) =>
                @emit Model.Signals.SendSuccess, data
