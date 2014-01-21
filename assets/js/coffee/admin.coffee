$ ->
  $("[data-delete-confirm]").on 'click', ->
    data = $(this).data 'rel'
    aElement = $("[data-dialog-url]")
    aElement.attr 'href', (aElement.attr 'href') + data + '/'
