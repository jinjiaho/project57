// anchor.js
anchors.options = {
	placement: "left"
};
anchors.add(".row h1");
anchors.add(".row h2");
anchors.add(".row h3");


// scrollspy.js (bootstrap)
$('body').scrollspy({
    target: '.bs-docs-sidebar',
    offset: 40
});
$(".bs-docs-sidebar").affix({
    offset: {
      top: 260
    }
});