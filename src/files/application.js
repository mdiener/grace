/**************************************************************************
 * Read up on jquery and joose for more info about the two libraries.
 *
 * You can put all your javascript files in to the "javascript" folder,
 * referencing them with a "//include path/to/file" (ommit the js) will
 * include the respective file.
 *
 * Ex.:
 * Folder structure
 * src
 *   javascipt
 *     MyClass.js
 *     utils
 *       MyUtilsClass.js
 *     MySecondClass.js
 *   application.js
 *
 * In your application.js, the first line would be: //include MyClass
 * In your MyClass.js the first line would be: //include MySecondClass.js
 * In your MySecondClass.js your would include the
 * Utils class: //include utils/MyUtilsClass
 *
 * The output will be the concatenated files, attached at the top of your
 * application.js file.
 *
 *************************************************************************/

jQuery(document).ready(function() {
    // start instantiating your main class here
});
