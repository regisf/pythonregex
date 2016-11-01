# _require "yesnodialog"
#
# Regex List
# Manage Use regex list
#

class RegexList
    constructor: (args) ->
        @useRegex = $ "#use-regex"
        @md = null

        $("[data-delete-regex]").on 'click', (evt) =>
            evt.preventDefault()

            if @md == null
                @md = new YesNoDialog("Delete regex", "Are you sure you want to delete this regular expression?")

            @md.on "yes", (e) =>
                id = evt.target.getAttribute('data-id')
                args.delete id, () ->
                    el = document.querySelector('tr[data-id="' + evt.target.getAttribute('data-id') + '"]')
                    el.parentNode.removeChild(el)

            @md.show()

        $("[data-use-regex]").on 'click', (e) =>
            e.preventDefault()
            selector = document.querySelector('tr[data-id="' + e.target.getAttribute('data-id') + '"]')
            args.use selector.querySelector('[data-regex-content]').textContent, e.target.getAttribute('data-name')

        return
