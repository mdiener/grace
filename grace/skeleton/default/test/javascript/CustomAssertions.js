QUnit.extend(QUnit.assert, {
    isString: function(str, msg) {
        var result = false;
        var actual = typeof str;
        if (actual === 'string') {
            result = true;
        }

        QUnit.push(result, actual, 'string', msg);
    },

    isBoolean: function(bool, msg) {
        var result = false;
        var actual = typeof bool;
        if (actual === 'boolean') {
            result = true;
        }

        QUnit.push(result, actual, 'boolean', msg);
    },

    isNumber: function(bool, msg) {
        var result = false;
        var actual = typeof bool;
        if (actual === 'number') {
            result = true;
        }

        QUnit.push(result, actual, 'number', msg);
    },

    isArray: function(arr, msg) {
        var result = false;
        var actual = typeof arr;
        if (actual === 'array') {
            result = true;
        }

        QUnit.push(result, actual, 'array', msg);
    },

    isObject: function(obj, msg) {
        var result = false;
        var actual = typeof obj;
        if (actual === 'object') {
            result = true;
        }

        QUnit.push(result, actual, 'object', msg);
    },

    isUndefined: function(undef, msg) {
        var result = false;
        var actual = typeof undef;
        if (actual === 'undefined') {
            result = true;
        }

        QUnit.push(result, actual, 'undefined', msg);
    },

    isNull: function(nul, msg) {
        var result = false;
        if (nul === null) {
            result = true;
        }

        QUnit.push(result, typeof nul, 'null', msg);
    },

    isInstanceOf: function(obj, cls, msg) {
        var result = false;
        if (obj instanceof cls) {
            result = true;
        }

        QUnit.push(result, obj, cls, msg);
    }
});
