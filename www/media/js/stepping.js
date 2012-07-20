function dotpath(p1, m1, p2, m2, hstep, vstep)  {
	return "M"+(p1+1)*hstep+","+(m1+1)*vstep+"L"+(p2+1)*hstep+","+(m2+1)*vstep;
}

$(function() {
	var	hsz, vsz, hstep, vstep;
	
	hsz = 800;
	vsz = 400;
	var paper = Raphael("display", hsz, vsz);
	
	//$('.display').appendChild(paper);
	
	
	var r;
	
	// 2 prime ideals
	//r = {"count": 2, "bases_vals": [[["0", "0"], ["2/3", "1/3"], ["4/3", "2/3"], ["2", "1"], ["8/3", "4/3"], ["10/3", "5/3"], ["49", "2"]], [["0", "0"], ["2/3", "1/3"], ["4/3", "2/3"], ["1", "5/2"], ["5/3", "17/6"], ["7/3", "19/6"], ["2", "49"]]], "j": [[1]], "n": 12, "ind_delta": [0, 0, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1], "phi_vals": [[["2/3", "1/3"], ["49", "2"]], [["2/3", "1/3"], ["1", "5/2"], ["2", "49"]]], "bases_inds": [[[0, 0], [0, 1], [0, 2], [0, 3], [0, 4], [0, 5], [1, 0]], [[0, 0, 0], [0, 0, 1], [0, 0, 2], [0, 1, 0], [0, 1, 1], [0, 1, 2], [1, 0, 0]]], "values": [["0", "0"], ["2/3", "1/3"], ["4/3", "2/3"], ["2", "1"], ["5/3", "17/6"], ["7/3", "19/6"], ["3", "7/2"], ["11/3", "23/6"], ["13/3", "25/6"], ["5", "9/2"], ["17/3", "29/6"], ["16/3", "152/3"]], "indices": [[0, 0], [1, 0], [1, 1], [1, 2], [1, 3], [2, 3], [3, 3], [4, 3], [5, 3], [5, 4], [5, 5], [5, 6]], "ns": [7, 7], "hidden": [[0, "2/3"], ["1/3", 0]], "types": [[{"h": 2, "e": 3, "f": 2}, {"h": 6, "e": 1, "f": 1}], [{"h": 1, "e": 3, "f": 1}, {"h": 9, "e": 2, "f": 1}, {"h": 12, "e": 1, "f": 1}]]};
	
	// 3 prime ideals
	r = {"count": 3, "bases_vals": [[["0", "0", "0"], ["2/3", "2/3", "1/2"], ["4/3", "4/3", "1"], ["2", "2", "3/2"], ["8/3", "8/3", "2"], ["10/3", "10/3", "5/2"], ["137", "4", "3"]], [["0", "0", "0"], ["2/3", "2/3", "1/2"], ["4/3", "4/3", "1"], ["2", "7/2", "3/2"], ["8/3", "25/6", "2"], ["10/3", "29/6", "5/2"], ["4", "137", "3"]], [["0", "0", "0"], ["2/3", "2/3", "1/2"], ["1", "1", "5/2"], ["5/3", "5/3", "3"], ["2", "2", "5"], ["8/3", "8/3", "11/2"], ["3", "3", "137"]]], "j": [[1, 1], [1]], "ind_delta": [0, 0, 2, 2, 0, 0, 0, 0, 0, 1, 1, 1, 2, 2, 1, 2, 2, 1], "n": 18, "phi_vals": [[["2/3", "2/3", "1/2"], ["137", "4", "3"]], [["2/3", "2/3", "1/2"], ["2", "7/2", "3/2"], ["4", "137", "3"]], [["2/3", "2/3", "1/2"], ["1", "1", "5/2"], ["3", "3", "137"]]], "bases_inds": [[[0, 0], [0, 1], [0, 2], [0, 3], [0, 4], [0, 5], [1, 0]], [[0, 0, 0], [0, 0, 1], [0, 0, 2], [0, 1, 0], [0, 1, 1], [0, 1, 2], [1, 0, 0]], [[0, 0, 0], [0, 0, 1], [0, 1, 0], [0, 1, 1], [0, 2, 0], [0, 2, 1], [1, 0, 0]]], "values": [["0", "0", "0"], ["2/3", "2/3", "1/2"], ["4/3", "4/3", "1"], ["5/3", "5/3", "3"], ["7/3", "7/3", "7/2"], ["3", "3", "4"], ["11/3", "11/3", "9/2"], ["13/3", "13/3", "5"], ["138", "5", "11/2"], ["416/3", "17/3", "6"], ["418/3", "19/3", "13/2"], ["140", "17/2", "7"], ["422/3", "55/6", "15/2"], ["141", "19/2", "19/2"], ["425/3", "61/6", "10"], ["427/3", "65/6", "21/2"], ["428/3", "67/6", "142"], ["430/3", "71/6", "285/2"]], "indices": [[0, 0, 0], [1, 0, 0], [1, 0, 1], [1, 0, 2], [2, 0, 2], [3, 0, 2], [4, 0, 2], [5, 0, 2], [6, 0, 2], [6, 1, 2], [6, 2, 2], [6, 3, 2], [6, 3, 3], [6, 3, 4], [6, 4, 4], [6, 4, 5], [6, 4, 6], [6, 5, 6]], "hidden": [[0, "2/3", "2/3"], ["2/3", 0, "2/3"], ["1/2", "1/2", 0]], "ns": [7, 7, 7], "types": [[{"h": 2, "e": 3, "f": 2}, {"h": 6, "e": 1, "f": 1}], [{"h": 2, "e": 3, "f": 1}, {"h": 9, "e": 2, "f": 1}, {"h": 12, "e": 1, "f": 1}], [{"h": 1, "e": 2, "f": 1}, {"h": 9, "e": 3, "f": 1}, {"h": 12, "e": 1, "f": 1}]]};
	
	console.log(r);
	
	var node, line;
	
	hstep = Math.floor(hsz / (r.count+1));
	vstep = Math.floor(vsz / (Math.max.apply(null, r.ns)+1));
	
	console.log(hstep, vstep);
	
	// Dots
	for (var s = 0; s < r.count; s++)  {
		for (var m = 0; m < r.ns[s]; m++)  {
			node = paper.circle((s+1)*hstep, (m+1)*vstep, 4);
			node.attr("fill", "#000000");
			node.hover(function() {
					this.attr({"fill": "#fff", "stroke-width": 2});
					this.transform("s1.5");
				},
				function ()  {
					this.attr({"fill": "#000", "stroke": "#000"});
					this.transform("s1");
				}
			);
		}
	}
	
	// Lines
	for (s = 1; s < r.count; s++)  {
		line = paper.path(dotpath(s-1, 0, s, 0, hstep, vstep));
		//line = paper.path("M"+(s)*hstep+","+vstep+"L"+(s+1)*hstep+","+vstep);
		line.attr({"stroke": "#6f6", "stroke-width": 1.5});
	}
	var olds = r.ind_delta[0];
	for (var i = 1; i < r.ind_delta.length; i++)  {
		var s = r.ind_delta[i];
		line = paper.path(dotpath(olds, r.indices[i-1][olds], s, r.indices[i][s], hstep, vstep));
		line.attr({"stroke": "#6f6", "stroke-width": 1.5});
		olds = s;

	}
	
	var text = paper.text(60, 30, "The potaroo\nsaid that!");
	console.log(text.width);
	
//	for (var i = 0; i < r.count; i++)  {
//		console.log(r.phi_vals[i]);
//	}
//	console.log(r.n, r.count);
//	
//	line = paper.path("M60,60L120,30");
//	line.attr({"stroke": "#000", "stroke-width": 1.5});
//	line = paper.path("M60,60L120,90");
//	line.attr({"stroke": "#000", "stroke-width": 1.5});
//	line = paper.path("M120,30L180,30");
//	line.attr({"stroke": "#000", "stroke-width": 1.5});
//	node = paper.circle(60, 60, 4);
//	
//	node.attr("fill", "#000000");
//	node.hover(function() {
//			this.attr({"fill": "#fff", "stroke-width": 2});
//			this.transform("s1.5");
//		},
//		function ()  {
//			this.attr({"fill": "#000", "stroke": "#000"});
//			this.transform("s1");
//		}
//	);
//	
//	node = paper.circle(120, 30, 3);
//	node.attr("fill", "#000000");
//	
//	
//	node = paper.circle(120, 90, 3);
//	node.attr("fill", "#000000");
//	
//	node = paper.circle(180, 30, 3);
//	node.attr("fill", "#000000");
//	
//	
//	
//	
//	var circle = paper.circle(50, 40, 10);
//	circle.attr("fill", "#f00");
//	circle.attr("stroke", "#fff");
//	
//	var jqcircle = $(circle);
//	
//	console.log($('#MathJax-Span-21'));
//		
//	var text = paper.text(60, 30, "The $3x$");
	
	
});