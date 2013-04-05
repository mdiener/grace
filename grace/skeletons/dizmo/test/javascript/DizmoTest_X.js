//include MyDizmo

var events = {}
var diz = new #PROJECTNAME.Dizmo();

QUnit.begin(function() {
    jQuery('#front').height(480);
    jQuery('#front').css('overflow', 'auto');
    jQuery('#front').css('-apple-dashboard-region', 'dashboard-region(control rectangle)');
});

QUnit.done(function() {
    dizmo.setAttribute('geometry/width', 1000);
    dizmo.setAttribute('geometry/height', 490);
});

test("Check if attributes are set correctly.", 4, function() {
    deepEqual(dizmo.getAttribute('geometry/width'), 250);
    deepEqual(dizmo.getAttribute('geometry/height'), 300);
    ok(dizmo.getAttribute('allowResize'), 'The allowResize attribute has been set correctly.');
    deepEqual('#PROJECTNAME', dizmo.getAttribute('title'), 'Title is equal');
})

asyncTest('Check if the resize event is being fired.', 1, function() {
    var size = dizmo.getSize();
    dizmo.setSize(200, 200);
    jQuery(events).on('dizmo.resize', function() {
        ok(true, 'Dizmo resize event has been fired correctly.');
        jQuery(events).off('dizmo.resize');
        start();
    });
})
