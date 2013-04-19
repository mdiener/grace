//include MyDizmo

var diz = new #PROJECTNAME.Dizmo();

test("Check if attributes are set correctly.", 1, function() {
    ok(dizmo.getAttribute('allowResize'), 'The allowResize attribute has been set correctly.')
})

asyncTest('Check if the resize event is being fired.', 1, function() {
    jQuery(events).on('dizmo.resize', function() {
        ok(true, 'Dizmo resize event has been fired correctly.');
        jQuery(events).off('dizmo.resize');
        start();
    });

    dizmo.setSize(300, 300);
})
