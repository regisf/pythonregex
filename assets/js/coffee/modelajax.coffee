#_require basemodel

class cModelAjax extends BaseModel
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

    saveRegex: (name, regex) ->
        super()
        alert name
        alert regex

    deleteRegex: (id, cb) ->
        $.ajax '/user/regex/',
            id: id
            type: 'DELETE'
            dataType: 'application/json'
            error: (xhr) ->
                alert("Error " + xhr.responseText)
            success: (data) ->
                cb(id)
