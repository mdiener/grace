Class('Dizmo.Utils.Docking', {
    methods: {
        /**
         * Get the side on which the docked dizmo has docked.
         * @param  {Object} otherDizmo A complete dizmo object (as provided by onDock, onUndock, canDock)
         * @return {String}              A string with either 'left', 'right', 'top', 'bottom'
         * @private
         */
        getDizmoPosition: function(mydizmo, otherDizmo) {
            if (typeof otherDizmo !== 'object') {
                throw {
                    name: 'mustBeADizmoObject',
                    message: 'You need to provide a dizmo object, as provided by onDock, onUndock or canDock.'
                };
            }

            try {
                var myRight = mydizmo.getAttribute('geometry/x');
                var myLeft = myRight - mydizmo.getAttribute('geometry/width');
                var myTop = mydizmo.getAttribute('geometry/y');
                var myBottom = myTop + mydizmo.getAttribute('geometry/height') + 40;
            } catch (e) {
                throw {
                    name: 'mustBeADizmoObject',
                    message: 'You need to provide a dizmo object, as provided by onDock, onUndock or canDock.'
                };
            }

            try {
                var otherRight = otherDizmo.getAttribute('geometry/x');
                var otherLeft = otherRight - otherDizmo.getAttribute('geometry/width');
                var otherTop = otherDizmo.getAttribute('geometry/y');
                var otherBottom = otherTop + otherDizmo.getAttribute('geometry/height') + 40;
            } catch (e) {
                throw {
                    name: 'mustBeADizmoObject',
                    message: 'You need to provide a dizmo object, as provided by onDock, onUndock or canDock.'
                };
            }

            if (otherRight <= myLeft) {
                return 'left';
            }

            if (otherLeft >= myRight) {
                return 'right';
            }

            if (otherBottom <= myTop) {
                return 'top';
            }

            if (otherTop >= myBottom) {
                return 'bottom';
            }
        }
    }
});

Class('Dizmo.Utils', {
    has: {
        'docking': {
            is: 'r',
            init: new Dizmo.Utils.Docking()
        }
    }
});

utils = new Dizmo.Utils();
