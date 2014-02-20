function dotpath(p1, m1, p2, m2, hstep, vstep)  {
	return "M"+(p1+1)*hstep+","+(m1+1)*vstep+"L"+(p2+1)*hstep+","+(m2+1)*vstep;
}

function html_bases_vals(r, s, m)  {
	var	vals, ind, html, sep;

	vals = r.bases_vals[s][m];
	ind = r.bases_inds[s][m];
	
	if (ind[0] == 1)
		vals[s] = '$\\pmb{\\infty}$';
	
	html = '$w(g_{'+(m)+','+prime_ideals[s]+'})$ = (';
	//html = '(';
	sep = '';
	
	for (var i = 0; i < vals.length; i++)  {
		if (i == s)
			val = '<span class="own-value">' + vals[i] + '</span>';
		else
			val = vals[i];
		html = html + sep + val;
		sep = ', ';
	}
	html = html + ')';
	
	return html;
}


function html_bases_vals_diff(r, s, m)  {
	var	vals, ind, html, sep;

	vals = r.bases_vals_diff[s][m];
	ind = r.bases_inds[s][m];
	
	if (ind[0] == 1)
		vals[s] = '$\\pmb{\\infty}$';
	
	html = '(';
	sep = '';
	
	for (var i = 0; i < vals.length; i++)  {
		if (String(vals[i]).substr(0, 1) != '-')
			vals[i] = '+' + vals[i];
		if (i == s)
			val = '<span class="own-value">' + vals[i] + '</span>';
		else
			val = vals[i];
		html = html + sep + val;
		sep = ', ';
	}
	html = html + ')';
	
	return html;
}

function phi_polynomial_html(r, s, m)  {
	var	ind, html, sep;

	ind = r.bases_inds[s][m];
	
//	if (ind[0] == 1)
//		vals[s] = '$\\infty$';
	
	html = '$g_{'+(m)+','+prime_ideals[s]+'} = ';
	sep = '';
	
	for (var i = 0; i < ind.length; i++)  {
		if (ind[i] > 0)  {
			var exp = '', phii = ind.length-i;
			if (ind[i] > 1)
				exp = '^{'+ind[i]+'}'
			if (i == 0)
				phii = prime_ideals[s];
			html = html + sep + '\\phi_{'+phii+'}'+exp;

			//sep = '\\cdot';
		}
	}
	if (m == 0)
		html = html + '1';
	html = html + '$';
	
	return html;
}

function html_basis_phi_polynomial(r, m)  {
	var indices = r.indices[m];
	var j, s, html, sep;

	html = '$g_{'+m+'} = ';
	sep = '';
	
	for (s = 0; s < indices.length; s++)  {
		html += sep + '(';
		var ind = r.bases_inds[s][indices[s]];

		var prime_html = '';
		for (var i = 0; i < ind.length; i++)  {
			if (ind[i] > 0)  {
				var exp = '', phii = ind.length-i;
				if (ind[i] > 1)
					exp = '^{'+ind[i]+'}'
				if (i == 0)
					phii = prime_ideals[s];
				else
					phii += ',' + prime_ideals[s];
				prime_html += '\\phi_{'+phii+'}'+exp;
			}
		}
		if (prime_html.length == 0)  {
			prime_html = '1';
		}

		//html += sep + vals[j];
		html += prime_html + ')';
	}
	html += '$'
	
	return html;


	/*var	ind, html, sep;

	ind = r.bases_inds[s][m];
	
	html = '$g_{'+(m)+','+prime_ideals[s]+'} = ';
	sep = '';
	
	for (var i = 0; i < ind.length; i++)  {
		if (ind[i] > 0)  {
			var exp = '', phii = ind.length-i;
			if (ind[i] > 1)
				exp = '^{'+ind[i]+'}'
			if (i == 0)
				phii = prime_ideals[s];
			html = html + sep + '\\phi_{'+phii+'}'+exp;

			//sep = '\\cdot';
		}
	}*/

}

function html_basis_val(r, i)  {
	vals = r.values[i];
	var j;
	
	for (j = 0; j < vals.length; j++)  {
		if (r.indices[i][j] == r.ns[j] - 1)
			vals[j] = '$\\infty$';
		if (r.indices.length > i+1 && r.indices[i][j] != r.indices[i+1][j])
			vals[j] = '<span class="minimum">'+vals[j]+'</span>';
	}
	
	html = '$w(g_{'+(i)+'})$ = (';
	sep = '';
	
	for (j = 0; j < vals.length; j++)  {
		html = html + sep + vals[j];
		sep = ', ';
	}
	html = html + ')';
	
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

function ideal_label_div(s)  {
	var labelId = 'label__ideal_'+s;
	var label = $('#'+labelId);
	if (label.length == 0)  {
		label = $('<div id="'+labelId+'" class="label"></div>');
		label.css({
			'left': (s+0.5)*hstep,
			'top': (0.5)*vstep,
			'width': hstep,
			'text-align': 'center'
		});
		//label.css('left', (s+0.5)*hstep).css('top', (0)*vstep).css('width', hstep).css('text-align', 'center');
		
		$('#display-upper').append(label);
	}
	
	return label;
}

function type_invariant_html(r, s, key)  {
	vals = r.types[s];
	
	html = '[';
	sep = '';

	for (var j = 0; j < vals.length; j++)  {
		html = html + sep + vals[j][key];
		
		sep = ', ';
	}
	
	html = html + ']';
	
	return html;
}

var hsz, vsz, paper;
var hstep, vstep;
var prime_ideals = [ ];

function max_length(r)  {
	var	max_length = 0;
	for (var s = 0; s < r.count; s++)  {
		if (r.bases_inds[s].length > max_length)
			max_length = r.bases_inds[s].length;
	}
	
	//console.log(max_length);
	
	return max_length;
}

function get_line_colour(invars)  {
	//console.log(invars.valid);
	if (invars.valid)  {
		if (invars.correct)
			return "#6c6";
		else
			return "#f33";
	}
	else  {
		if (invars.correct)
			return "#6ff";
		else
			return "#f3f";
	}
}

function draw_stepping(invars)  {
	var	r;

	r = invars;
	line_colour = get_line_colour(r);
	
	$('#display').height((max_length(r)+1)*110);
	hsz = $('#display').width();
	vsz = $('#display').height();
	$('#display').empty();
	paper = Raphael("display", hsz, vsz);
	
	paper.clear();
	var overlay = $('#display-outer');
	overlay.children('.label').remove();
	$('#display-upper').children().remove();
	
	var node, line;
	var values, polynomials;
	
	hstep = Math.floor(hsz / (r.count+1));
	vstep = Math.floor(vsz / (Math.max.apply(null, r.ns)+1));
	
	if (r.primes)  {
		prime_ideals = [ ];
		for (var i in r.primes)  {
			prime_ideals[i] = '\\mathfrak{' + r.primes[i] + '}';
		}
	}
	else if (r.count == 2)  {
		prime_ideals = ['\\mathfrak{p}', '\\mathfrak{q}'];
	}
	else if (r.count == 3) {
		prime_ideals = ['\\mathfrak{p}', '\\mathfrak{q}', '\\mathfrak{l}'];
	}
	else if (r.count == 4) {
		prime_ideals = ['\\mathfrak{p}', '\\mathfrak{q}', '\\mathfrak{r}', '\\mathfrak{s}'];
	}
	else {
		prime_ideals = [ ];
		for (var s = 0; s < r.count; s++)
			prime_ideals[s] = '\\mathfrak{p_{'+(s+1)+'}}';
	}
	
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
			values = $('<span class="values phi-polynomial"></span>');
			values.append(phi_polynomial_html(r, s, m));
			label = label_div(s, m);
			label.append(values);
			values = $('<span class="values bases-values switcher"></span>');
			values.append($('<span class="1" style="display: inline;"></span>').append(html_bases_vals(r, s, m)));
			values.append($('<span class="2" style="display: none;"></span>').append(html_bases_vals_diff(r, s, m)));
			label.append('<br />', values);
			
			values.bind('click', function() {
				var	max = 0, current = -1;
			});
			
//			values = $('<span class="values bases-values-diff"></span>');
//			values.append(html_bases_vals_diff(r, s, m));
//			label.append(' / ', values);
			
			
			//label = $('<div id="label__'+r+'_'+s+'" class="label"></div>');
			//label.css('left', (s+1)*hstep).css('top', (m+1)*vstep);
		}
	}
	
	for (s = 0; s < r.count; s++)  {
		label = ideal_label_div(s);
		var ideal = $('<div class="ideal">$'+prime_ideals[s]+'$</div>');
		label.append(ideal);
		label.append('e = ' + type_invariant_html(r, s, 'e'));
		label.append('<br />', 'f = ' + type_invariant_html(r, s, 'f'));
		label.append('<br />', 'h = ' + type_invariant_html(r, s, 'h'));
	}
	
	// Lines
	for (s = 1; s < r.count; s++)  {
		line = paper.path(dotpath(s-1, 0, s, 0, hstep, vstep));
		line.attr({"stroke": line_colour, "stroke-width": 1.5, 'stroke-dasharray': ['-']});
		
		label = label_div(s, 0);
		polynomials = $('<span class="polynomials basis-polynomials"></span>');
		polynomials.append(html_basis_phi_polynomial(r, 0));
		label.append('<br/>', polynomials);
		values = $('<span class="values basis-values"></span>');
		values.append(html_basis_val(r, 0));
		label.append('<br />', values);
	}
	label = label_div(0, 0);
	polynomials = $('<span class="polynomials basis-polynomials"></span>');
	polynomials.append(html_basis_phi_polynomial(r, 0));
	label.append('<br/>', polynomials);
	values = $('<span class="values basis-values"></span>');
	values.append(html_basis_val(r, 0));
	label.append('<br />', values);
	
	var olds = r.ind_delta[0];
	for (var i = 1; i < r.ind_delta.length; i++)  {
		var s = r.ind_delta[i];
		line_arrow = paper.arrow((olds+1)*hstep, (r.indices[i-1][olds]+1)*vstep, (s+1)*hstep, (r.indices[i][s]+1)*vstep, 4);
		line_arrow[0].attr({"arrow-end": "classic-long", "stroke": line_colour, "stroke-width": 1.5});
		if (i == r.ind_delta.length-1)
			line_arrow[0].attr({"stroke-dasharray": ["-"]})
		line_arrow[1].attr({"arrow-end": "classic-long", "stroke": line_colour, "fill": line_colour});
		//line = paper.path(dotpath(olds, r.indices[i-1][olds], s, r.indices[i][s], hstep, vstep));
		//line.attr({"stroke": "#6f6", "stroke-width": 1.5});
		olds = s;
		
		label = label_div(s, r.indices[i][s]);
		polynomials = $('<span class="polynomials basis-polynomials"></span>');
		polynomials.append(html_basis_phi_polynomial(r, i));
		label.append('<br/>', polynomials);
		values = $('<span class="values basis-values"></span>');
		values.append(html_basis_val(r, i));
		label.append('<br />', values);
	}
	var s;
	for (s = 0; s < r.count; s++)  {
		if (r.indices[r.indices.length-1][s] < r.ns[s]-1)
			break;
	}
/*	line_arrow = paper.arrow((olds+1)*hstep, (r.indices[r.indices.length-1][olds]+1)*vstep, (s+1)*hstep, (r.ns[s])*vstep, 4);
	line_arrow[0].attr({"arrow-end": "classic-long", "stroke": line_colour, "stroke-width": 1.5, 'stroke-dasharray': ['-']});
	line_arrow[1].attr({"arrow-end": "classic-long", "stroke": line_colour, "fill": line_colour});*/

	if (r.error)  {
		$('.error').empty().append(r.error).css('display', 'block');
	}
	else  {
		$('.error').empty().css('display', 'none');
	}

	$('#__id_vs_log').val(r.vs_log);
	prettify_inv();

	MathJax.Hub.Queue(["Typeset",MathJax.Hub]);	
}

function prettify_inv()  {
	var nice_inv = JSON.stringify(JSON.parse($('#id__textarea').val()), replacer, 2);
	var fixed_nice_inv = "";
	var lines = nice_inv.split("\n");
	for (var i in lines)  {
		line = lines[i];
		if (line.match(/^\s+("\w+":\s+)?"UnStr\<\</))  {
			line = line.replace(/"UnStr\<\<(.+?)\>\>"/, "$1").replace(/\\"/g, "\"").replace(/(,|:)/g, "$1 "); 
		}
		fixed_nice_inv += line + "\n";
	}
	
	$('#id__textarea').val(fixed_nice_inv);
}

function replacer(key, value)  {
	var last_level = false;
	if (typeof(value) == "object")  {
		if (value instanceof Array)  {
			last_level = true;
			for (var i = 0; i < value.length; i++)  {
				if (typeof(value[i]) == "object")  {
					last_level = false;
					break;
				}
			}
		}
		else  {
			last_level = true;
			for (var k in value)  {
				if (typeof(value[k]) == "object")  {
					last_level = false;
					break;
				}
			}
		}
	}

	if (last_level)  {
		return "UnStr<<" + JSON.stringify(value, undefined, 0) + ">>";
	}
	else  {
		return value;
	}
}

function change_r()  {
	var i = $(this).attr('id').match(/id__subgroup_invariants_(\d+)/)[1];
		
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
			//console.log(data);
			draw_stepping(data);
		},
	});
	
}

function fetch_stepping_invars_textarea()  {
	fetch_stepping_invars($('#id__textarea').val());
}

function ind_coin(inv, i, j)  {
	if (i > j)  {
		var t = j;
		j = i;
		i = t;
	}
	
	return inv.j[i][j-i-1];	
}

function drawTree(inv)  {
	
	var types = [ ];
	var max_r = 0;
	
	//console.log(inv);
	for (var ti = 0; ti < inv.types.length; ti++)  {
		if (inv.types[ti].length > max_r)  {
			max_r = inv.types[ti].length;
		}
	
	}
	
	for (var i = 0; i < inv.types.length; i++)  {
		for (var j = i+1; j < inv.types.length; j++)  {
			//console.log("index of coincidence", i, j, "=", ind_coin(inv, i, j));
		}
	}
	
//	node = paper.circle((s+1)*hstep, (m+1)*vstep, 4);
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
	
}

function load_template(template)  {
	var template_div = $('#id__'+template);
	var textarea = $('#id__textarea');
	
	textarea.val(template_div.contents().text());
}

function switch_to(v)  {
	$('.switcher').children().css({'display': 'none'});
	$('.switcher .'+v).css({'display': 'inline'});
}

$(function() {
	//var	hsz, vsz, hstep, vstep;
	
	hsz = $('#display').width();
	vsz = $('#display').height();
	paper = Raphael("display", hsz, vsz);
	
	//$('.display').appendChild(paper);
	
	
	var r;

	$('#id__invariant_form').bind('submit', function()  { fetch_stepping_invars_textarea(); return false; });
	
	var inv = '{"hidden": [[0, 0, 0], [0, 0, 0], [0, 0, 0]], "j": [[2, 1], [1]], "types": [[{"h": 2, "e": 3, "f": 2}, {"h": 6, "e": 1, "f": 1}], [{"h": 2, "e": 3, "f": 1}, {"h": 9, "e": 2, "f": 1}, {"h": 12, "e": 1, "f": 1}], [{"h": 1, "e": 2, "f": 1}, {"h": 9, "e": 3, "f": 1}, {"h": 12, "e": 1, "f": 1}]]}';
	//fetch_stepping_invars(inv)
	fetch_stepping_invars_textarea();
	
	//drawTree(JSON.parse(inv));
	
	
	
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
	

});

Raphael.fn.arrow = function (x1, y1, x2, y2, size) {
    var angle = Math.atan2(x1-x2,y2-y1);
    angle = (angle / (2 * Math.PI)) * 360;
    var arrowPath = this.path("M" + x2 + " " + y2 + " L" + (x2 - size*3) + " " + (y2 - size) + " L" + (x2 - size*3) + " " + (y2 + size) + " L" + x2 + " " + y2 ).attr("fill","black").rotate((90+angle),x2,y2);
    var linePath = this.path("M" + x1 + " " + y1 + " L" + x2 + " " + y2);
    return [linePath,arrowPath];
}
