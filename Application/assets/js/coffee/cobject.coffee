###
Signal/Slot object
###

class cObject
    constructor: ->
        @sig = []

    # Connect the object to a signal
    connect: (signal, slot) ->
        if signal and slot
            @sig.push { signal: signal, slot: slot }
        @

    # Emit a signal
    emit: (signal, args) ->
        for ss in @sig
            if ss.signal is signal
                ss.slot args
        @
