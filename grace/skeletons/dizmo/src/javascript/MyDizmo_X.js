Class("#PROJECTNAME.Dizmo", {
    after: {
        initialize: function() {
            var me = this;

            // Show front and hide back on first load
            jQuery("#back").hide();
            jQuery("#front").show();

            me._setAttributes();
            me._initEvents();

            me._restore();
        }
    },

    methods: {
        /**
         * Initiate all the events for dizmo related stuff
         */
        _initEvents: function() {
            // Show back and front listeners
            dizmo.onShowBack(function() {
                jQuery("#front").hide();
                jQuery("#back").show();
            });

            dizmo.onShowFront(function() {
                jQuery("#back").hide();
                jQuery("#front").show();
            });

            // Subscribe to height changes of the dizmo
            dizmo.subscribeToAttribute('geometry/height', function(path, val, oldVal) {
                if (val < 200) {
                    dizmo.setAttribute('geometry/height', 200);
                }

                dizmo.privateStorage().setProperty('height', val);
                jQuery(events).trigger('dizmo.resize');
            });

            // Subscribe to width changes of the dizmo
            dizmo.subscribeToAttribute('geometry/width', function(path, val, oldVal) {
                if (val < 200) {
                    dizmo.setAttribute('geometry/width', 200);
                }

                dizmo.privateStorage().setProperty('width', val);
                jQuery(events).trigger('dizmo.resize');
            });

            // Subscribe to displayMode changes
            viewer.subscribeToAttribute('displayMode', function(path, val, oldVal) {
                if (val === 'presentation') {
                    dizmo.setAttribute('hideframe', true);
                    jQuery(events).trigger('dizmo.display', [true]);
                } else {
                    dizmo.setAttribute('hideframe', false);
                    jQuery(events).trigger('dizmo.display', [false]);
                }
            });
        },

        /**
         * Restore the saved dizmo state (width, height)
         * @private
         */
        _restore: function() {
            if (dizmo.privateStorage().getProperty('width')) {
                dizmo.setAttribute('geometry/width', parseInt(dizmo.privateStorage().getProperty('width')));
            }

            if (dizmo.privateStorage().getProperty('height')) {
                dizmo.setAttribute('geometry/height', parseInt(dizmo.privateStorage().getProperty('height')));
            }
        },

        /**
         * Set the dizmo default attributes like resize and docking
         * @private
         */
        _setAttributes: function() {
            dizmo.setAttribute('allowResize', true);
            dizmo.canDock(function() {
                return false;
            });
        },

        /**
         * Shows the back of the dizmo
         * @public
         */
        showBack: function() {
            dizmo.showBack();
        },

        /**
         * Shows the front of the dizmo
         * @public
         */
        showFront: function() {
            dizmo.showFront();
        }
    }
});
