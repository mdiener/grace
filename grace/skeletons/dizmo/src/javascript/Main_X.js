Class("#PROJECTNAME.Main", {
    after: {
        initialize: function(dizmo) {
            var me = this;

            me._dizmo = dizmo;
            me._initEvents();
        }
    },

    methods: {
        _initEvents: function() {
            var me = this;

            jQuery('.done-btn').on('click', function() {
                me._dizmo.showFront();
            });
        }
    }
});
