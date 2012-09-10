function dotpath(p1, m1, p2, m2, hstep, vstep)  {
	return "M"+(p1+1)*hstep+","+(m1+1)*vstep+"L"+(p2+1)*hstep+","+(m2+1)*vstep;
}

function html_bases_vals(r, s, m)  {
	var	vals, ind, html, sep;

	vals = r.bases_vals[s][m];
	ind = r.bases_inds[s][m];
	
	if (ind[0] == 1)
		vals[s] = '$\\infty$';
	
	//console.log(ind, vals);
	html = '(';
	sep = '';
	
	for (var i = 0; i < vals.length; i++)  {
		html = html + sep + vals[i];
		sep = ', ';
	}
	html = html + ')';
	
	return html;
}

function html_basis_val(r, i)  {
	vals = r.values[i];
	
	html = '(';
	sep = '';
	
	
	
	for (var j = 0; j < vals.length; j++)  {
		html = html + sep + vals[j];
		sep = ', ';
	}
	html = html + ')';
	
	//console.log(r.values[i], html);
	
	return html;
}

function label_div(s, m)  {
	var labelId = 'label__'+s+'_'+m;
	var label = $('#'+labelId);
	if (label.length == 0)  {
		label = $('<div id="'+labelId+'" class="label"></div>');
		label.css('left', (s+1)*hstep).css('top', (m+1)*vstep);
		
		$('#display-outer').append(label);
	}
	
	return label;
}

var hsz, vsz, paper;
var hstep, vstep;

function draw_stepping(invars)  {
	var	r;
	
	paper.clear();
	var overlay = $('#display-outer');
	overlay.children('.label').remove();
	
	r = invars;
	
	console.log(r.bases_inds);

	//console.log(r);
	//console.log(hsz, vsz, r.count);
	
	var node, line;
	
	hstep = Math.floor(hsz / (r.count+1));
	vstep = Math.floor(vsz / (Math.max.apply(null, r.ns)+1));
	
	//console.log(hstep, vstep);
	
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
			
			values = $('<span class="values bases-values"></span>');
			//html_bases_vals(r, s, m);
			values.append(html_bases_vals(r, s, m));
			label = label_div(s, m);
			label.append(values);			
			//label = $('<div id="label__'+r+'_'+s+'" class="label"></div>');
			//label.css('left', (s+1)*hstep).css('top', (m+1)*vstep);
		}
	}
	
	// Lines
	for (s = 1; s < r.count; s++)  {
		line = paper.path(dotpath(s-1, 0, s, 0, hstep, vstep));
		//line = paper.path("M"+(s)*hstep+","+vstep+"L"+(s+1)*hstep+","+vstep);
		line.attr({"stroke": "#6f6", "stroke-width": 1.5});
		
		values = $('<span class="values basis-values"></span>');
		values.append(html_basis_val(r, 0));
		label = label_div(s, 0);
		label.append('<br />', values);
	}
	values = $('<span class="values basis-values"></span>');
	values.append(html_basis_val(r, 0));
	label = label_div(0, 0);
	label.append('<br />', values);
	
	var olds = r.ind_delta[0];
	for (var i = 1; i < r.ind_delta.length; i++)  {
		var s = r.ind_delta[i];
		line = paper.path(dotpath(olds, r.indices[i-1][olds], s, r.indices[i][s], hstep, vstep));
		line.attr({"stroke": "#6f6", "stroke-width": 1.5});
		olds = s;
		
		values = $('<span class="values basis-values"></span>');
		values.append(html_basis_val(r, i));
		label = label_div(s, r.indices[i][s]);
		label.append('<br />', values);
	}
	
	MathJax.Hub.Queue(["Typeset",MathJax.Hub]);	
}

function change_r()  {
	var i = $(this).attr('id').match(/id__subgroup_invariants_(\d+)/)[1];
	console.log("new r value for index: " + i);
	
	var group = ('#id__subgroup_invariants_'+i);
}

function create_invar_groups()  {
	var		s;
	
	s = $('#id__num_prime_ideals').val();
	
	var inv_root = $('#id__group_invariants');
	
	inv_root.empty();
	
	inv_root.append('<textarea id="id__textarea" cols="40" rows="20"></textarea>');
	
	var textarea = inv_root.children('textarea');
	
	var inv = { 'types': [ [ {'e': 3, 'f': 2, 'h': 2}, {'e': 1, 'f': 1, 'h': 6}, ], ] };
	textarea.append(JSON.stringify(inv));
	
	
/*	for (var i = 1; i <= s; i++)  {
		inv_root.append('<div id="id__subgroup_invariants_'+i+'" class="subgroup_invariants"><p><label for="id__r_'+i+'">$r_{'+i+'}$</label>: <input type="text" id="id__r_'+i+'" value="2" size="2" /></p></div>');
		
		var group = $('#id__subgroup_invariants_'+i);
		//group_p = group.append('<p class="invars"></p>').children('p.invars');
		for (var j = 1; j <= 2; j++)  {
			var group_p = group.append('<p></p>').children('p').last();
			group_p.append(
				'<label class="invar" for="id__e_'+i+'_'+j+'">$e_{'+i+','+j+'}$</label>: <input id="id__e_'+i+'_'+j+'" type="text" size="1" />',
				'<label class="invar" for="id__f_'+i+'_'+j+'">$f_{'+i+','+j+'}$</label>: <input id="id__f_'+i+'_'+j+'" type="text" size="1" />',
				'<label class="invar" for="id__h_'+i+'_'+j+'">$h_{'+i+','+j+'}$</label>: <input id="id__h_'+i+'_'+j+'" type="text" size="1" />');
		}	
	}
	
	$('.subgroup_invariants').bind('change', change_r);*/
	
	
	MathJax.Hub.Queue(["Typeset",MathJax.Hub]);
}

function fetch_stepping_invars(inv)  {
	//inv = inv.replace(/\s+/g, '');
	$.ajax({
		url: '/stepping/?inv='+inv,
		success: function(data)  {
			console.log(data);
			draw_stepping(data);
		},
	});
	
}

function fetch_stepping_invars_textarea()  {
	fetch_stepping_invars($('#id__textarea').val());
}

$(function() {
	//var	hsz, vsz, hstep, vstep;
	
	hsz = $('#display').width();
	vsz = $('#display').height();
	paper = Raphael("display", hsz, vsz);
	
	//$('.display').appendChild(paper);
	
	
	var r;

	$('#id__invariant_form').bind('submit', function()  { fetch_stepping_invars_textarea(); return false; });
	
	var inv = '{"hidden": [[0, 0, 0], [0, 0, 0], [0, 0, 0]], "j": [[1, 1], [1]], "types": [[{"h": 2, "e": 3, "f": 2}, {"h": 6, "e": 1, "f": 1}], [{"h": 2, "e": 3, "f": 1}, {"h": 9, "e": 2, "f": 1}, {"h": 12, "e": 1, "f": 1}], [{"h": 1, "e": 2, "f": 1}, {"h": 9, "e": 3, "f": 1}, {"h": 12, "e": 1, "f": 1}]]}';
	fetch_stepping_invars(inv)
	
	
	//$('#id__num_prime_ideals').bind('change', create_invar_groups);
	
	
	// 2 prime ideals
	//r = {"count": 2, "bases_vals": [[["0", "0"], ["2/3", "1/3"], ["4/3", "2/3"], ["2", "1"], ["8/3", "4/3"], ["10/3", "5/3"], ["49", "2"]], [["0", "0"], ["2/3", "1/3"], ["4/3", "2/3"], ["1", "5/2"], ["5/3", "17/6"], ["7/3", "19/6"], ["2", "49"]]], "j": [[1]], "n": 12, "ind_delta": [0, 0, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1], "phi_vals": [[["2/3", "1/3"], ["49", "2"]], [["2/3", "1/3"], ["1", "5/2"], ["2", "49"]]], "bases_inds": [[[0, 0], [0, 1], [0, 2], [0, 3], [0, 4], [0, 5], [1, 0]], [[0, 0, 0], [0, 0, 1], [0, 0, 2], [0, 1, 0], [0, 1, 1], [0, 1, 2], [1, 0, 0]]], "values": [["0", "0"], ["2/3", "1/3"], ["4/3", "2/3"], ["2", "1"], ["5/3", "17/6"], ["7/3", "19/6"], ["3", "7/2"], ["11/3", "23/6"], ["13/3", "25/6"], ["5", "9/2"], ["17/3", "29/6"], ["16/3", "152/3"]], "indices": [[0, 0], [1, 0], [1, 1], [1, 2], [1, 3], [2, 3], [3, 3], [4, 3], [5, 3], [5, 4], [5, 5], [5, 6]], "ns": [7, 7], "hidden": [[0, "2/3"], ["1/3", 0]], "types": [[{"h": 2, "e": 3, "f": 2}, {"h": 6, "e": 1, "f": 1}], [{"h": 1, "e": 3, "f": 1}, {"h": 9, "e": 2, "f": 1}, {"h": 12, "e": 1, "f": 1}]]};
	
	// 3 prime ideals
	r = {
		"count": 3,
		"bases_vals": [[["0", "0", "0"], ["2/3", "2/3", "1/2"], ["4/3", "4/3", "1"], ["2", "2", "3/2"], ["8/3", "8/3", "2"], ["10/3", "10/3", "5/2"], ["137", "4", "3"]], [["0", "0", "0"], ["2/3", "2/3", "1/2"], ["4/3", "4/3", "1"], ["2", "7/2", "3/2"], ["8/3", "25/6", "2"], ["10/3", "29/6", "5/2"], ["4", "137", "3"]], [["0", "0", "0"], ["2/3", "2/3", "1/2"], ["1", "1", "5/2"], ["5/3", "5/3", "3"], ["2", "2", "5"], ["8/3", "8/3", "11/2"], ["3", "3", "137"]]],
		"j": [[1, 1], [1]],
		"ind_delta": [0, 0, 2, 2, 0, 0, 0, 0, 0, 1, 1, 1, 2, 2, 1, 2, 2, 1],
		"n": 18,
		"phi_vals": [[["2/3", "2/3", "1/2"], ["137", "4", "3"]], [["2/3", "2/3", "1/2"], ["2", "7/2", "3/2"], ["4", "137", "3"]], [["2/3", "2/3", "1/2"], ["1", "1", "5/2"], ["3", "3", "137"]]],
		"bases_inds": [[[0, 0], [0, 1], [0, 2], [0, 3], [0, 4], [0, 5], [1, 0]], [[0, 0, 0], [0, 0, 1], [0, 0, 2], [0, 1, 0], [0, 1, 1], [0, 1, 2], [1, 0, 0]], [[0, 0, 0], [0, 0, 1], [0, 1, 0], [0, 1, 1], [0, 2, 0], [0, 2, 1], [1, 0, 0]]],
		"values": [["0", "0", "0"], ["2/3", "2/3", "1/2"], ["4/3", "4/3", "1"], ["5/3", "5/3", "3"], ["7/3", "7/3", "7/2"], ["3", "3", "4"], ["11/3", "11/3", "9/2"], ["13/3", "13/3", "5"], ["138", "5", "11/2"], ["416/3", "17/3", "6"], ["418/3", "19/3", "13/2"], ["140", "17/2", "7"], ["422/3", "55/6", "15/2"], ["141", "19/2", "19/2"], ["425/3", "61/6", "10"], ["427/3", "65/6", "21/2"], ["428/3", "67/6", "142"], ["430/3", "71/6", "285/2"]],
		"indices": [[0, 0, 0], [1, 0, 0], [1, 0, 1], [1, 0, 2], [2, 0, 2], [3, 0, 2], [4, 0, 2], [5, 0, 2], [6, 0, 2], [6, 1, 2], [6, 2, 2], [6, 3, 2], [6, 3, 3], [6, 3, 4], [6, 4, 4], [6, 4, 5], [6, 4, 6], [6, 5, 6]],
		"hidden": [[0, "2/3", "2/3"], ["2/3", 0, "2/3"], ["1/2", "1/2", 0]],
		"ns": [7, 7, 7],
		"types": [[{"h": 2, "e": 3, "f": 2}, {"h": 6, "e": 1, "f": 1}], [{"h": 2, "e": 3, "f": 1}, {"h": 9, "e": 2, "f": 1}, {"h": 12, "e": 1, "f": 1}], [{"h": 1, "e": 2, "f": 1}, {"h": 9, "e": 3, "f": 1}, {"h": 12, "e": 1, "f": 1}]]
	};
	
/*	console.log(r);
	
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
			
			values = $('<span class="values"></span>');
			html_bases_vals(r, s, m);
			values.append(html_bases_vals(r, s, m));
			label = $('<div class="label"></div>');
			label.append(values);
			$('#display-outer').append(label);
			label.css('left', (s+1)*hstep).css('top', (m+1)*vstep);
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
		
		var label, values;
		

	}
	
	//var text = paper.text(60, 30, "The potaroo\nsaid that!");
	//console.log(text.width);
	
	
*/	
});