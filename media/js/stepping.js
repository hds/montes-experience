$(function() {

	var paper = Raphael("display", 320, 200);
	
	//$('.display').appendChild(paper);
	
	var circle = paper.circle(50, 40, 10);
	circle.attr("fill", "#f00");
	circle.attr("stroke", "#fff");
});