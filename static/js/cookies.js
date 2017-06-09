/**
 *   === cookies.js ===
 *
 *   A complete cookie reader/writer framework with full unicode support.
 * 
 *   Public methods:
 * 
 *   - docCookies.setItem(name, value[, end[, path[, domain[, secure]]]]) - Create/overwrite a cookie
 *   - docCookies.getItem(name)                                           - Read a cookie. If a cookies doesn't exist a null value is returned
 *   - docCookies.removeItem(name[, path[, domain]])                      - Delete a cookie
 *   - docCookies.hasItem(name)                                           - Check if a cookie exists in the current position
 *   - docCookies.keys()                                                  - Return an array of all readable cookies from this location
 *
 *
 *   --------------------------------------
 *        Last modified: 7 June 2017     
 *   --------------------------------------
 */

var docCookies = {

  /**
	 * Read a cookie. If a cookies doesn't exist a null value will be returned
	 *
	 * @param {string} sKey - Name of cookie
	 * @return {string} Value of cookie if present, else null
	 */
  getItem: function (sKey) {
    if (!sKey) { return null; }
    return decodeURIComponent(document.cookie.replace(new RegExp("(?:(?:^|.*;)\\s*" + encodeURIComponent(sKey).replace(/[\-\.\+\*]/g, "\\$&") + "\\s*\\=\\s*([^;]*).*$)|^.*$"), "$1")) || null;
  },

  /**
	 * Create/overwrite a cookie
	 *
	 * @param {string}                 sKey - Name of cookie to create/overwrite
	 * @param {string}               sValue - Value of the cookie
	 * @param {number, Infinity, Date} vEnd - Max age in seconds as an integer, an Infinity or Date object; defaults to end of session time
	 * @param {string}                sPath - Path from where cookie will be readable; defaults to path of current document location
	 * @param {string}              sDomain - Domain from where cookie will be readable; defaults to current document host
	 * @param {boolean}             bSecure - Set secure cookie transmission over HTTPS
	 */
  setItem: function (sKey, sValue, vEnd, sPath, sDomain, bSecure) {
    if (!sKey || /^(?:expires|max\-age|path|domain|secure)$/i.test(sKey)) { return false; }
    var sExpires = "";
    if (vEnd) {
      switch (vEnd.constructor) {
        case Number:
          sExpires = vEnd === Infinity ? "; expires=Fri, 31 Dec 9999 23:59:59 GMT" : "; max-age=" + vEnd;
          break;
        case String:
          sExpires = "; expires=" + vEnd;
          break;
        case Date:
          sExpires = "; expires=" + vEnd.toUTCString();
          break;
      }
    }
    document.cookie = encodeURIComponent(sKey) + "=" + encodeURIComponent(sValue) + sExpires + (sDomain ? "; domain=" + sDomain : "") + (sPath ? "; path=" + sPath : "") + (bSecure ? "; secure" : "");
    return true;
  },

  /**
	 * Delete a cookie
	 *
	 * @param {string}    sKey - Name of cookie to remove
	 * @param {string}   sPath - Path from where cookie will be removed; defaults to path of current document location
	 * @param {string} sDomain - Domain from where cookie will be removed; defaults to current document host
	 */
  removeItem: function (sKey, sPath, sDomain) {
    if (!this.hasItem(sKey)) { return false; }
    document.cookie = encodeURIComponent(sKey) + "=; expires=Thu, 01 Jan 1970 00:00:00 GMT" + (sDomain ? "; domain=" + sDomain : "") + (sPath ? "; path=" + sPath : "");
    return true;
  },

  /**
	 * Check if a cookie exists in the current position
	 *
	 * @param {string} sKey - Name of cookie to test
	 * @return {boolean} True if cookie is present, else false
	 */
  hasItem: function (sKey) {
    if (!sKey) { return false; }
    return (new RegExp("(?:^|;\\s*)" + encodeURIComponent(sKey).replace(/[\-\.\+\*]/g, "\\$&") + "\\s*\\=")).test(document.cookie);
  },

  /**
	 * Return an array of all readable cookies from this location
	 *
	 * @return {Array} Array of all readable cookies from this location
	 */
  keys: function () {
    var aKeys = document.cookie.replace(/((?:^|\s*;)[^\=]+)(?=;|$)|^\s*|\s*(?:\=[^;]*)?(?:\1|$)/g, "").split(/\s*(?:\=[^;]*)?;\s*/);
    for (var nLen = aKeys.length, nIdx = 0; nIdx < nLen; nIdx++) { aKeys[nIdx] = decodeURIComponent(aKeys[nIdx]); }
    return aKeys;
  }

};

