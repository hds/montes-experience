import sys

import Image, ImageDraw, ImageFont

import fractions
import math
import operator
from operator import mul
import numbers
import json
from json.encoder import JSONEncoder
Rational = numbers.Rational
        

class Rat (fractions.Fraction):
    def __repr__(self):
        if self._denominator == 1:
            return "%d" % (self._numerator,)
        else:
            return self.__str__()

class SteppingJSONEncoder(JSONEncoder):
    
    def default(self, o):
        if isinstance(o, Rat):
            return str(repr(o))
        return JSONEncoder.default(self, o)

def rat(n, d):
    return Rat(n, d)

def frac2rat(f):
    return Rat(f._numerator, f._denominator)

def prod(l):
    return reduce(mul, l, 1)

def V_i(tt, i):
    if i == 1:
        return 0
    else:
        i -= 1
        return tt[i-1]['e'] * tt[i-1]['f'] * (tt[i-1]['e'] * V_i(tt, i) + tt[i-1]['h'])

def m_i(tt, i):
    return prod([t['e']*t['f'] for t in tt[0:i-1]])

def p_val(tt, i):
    return rat(V_i(tt, i) + rat(tt[i-1]['h'], tt[i-1]['e']), prod([t['e'] for t in tt[0:i-1]]))

def c_val(ptt, stt, i, j, hidden):
    if i < j:
        return p_val(ptt, i)
    elif i == j:
        if hidden[0] == rat(ptt[j-1]['h'], ptt[j-1]['e']):
            lam = hidden[1]
        else:
            lam = min(hidden)
        return rat(V_i(ptt, j) + lam, prod([t['e'] for t in ptt[0:j-1]]))
    else:
        min_lam = min(hidden)
        j_val = rat(V_i(ptt, j) + min_lam, prod([t['e'] for t in ptt[0:j-1]]))
        return rat(m_i(ptt, i), m_i(ptt, j)) * j_val

def phi_val(invars, s, r, i):
    val = 0
    if s == r:
        val = p_val(invars['types'][s], i)
    else:
        j = fetch_j(invars, s, r)
        hidden = fetch_hidden(invars, s, r)
        val = c_val(invars['types'][s], invars['types'][r], i, j, hidden)

    return val

def phi_values(invars):
    phi_vals = [ [] for t in invars['types'] ]

    for s in range(0, len(invars['types'])):
        tt = invars['types'][s]
        for i in range(1, len(tt)+1):
            vals = [ frac2rat(phi_val(invars, s, r, i)) for r in range(0, len(invars['types'])) ]
            phi_vals[s].append(vals)
            #print [ s, r, i, vals ]
            #for r in range(0, len(invars['types'])):

    return phi_vals

def basis_values(invars, phi_vals, s, d):
    if d == 0:
        d = len(phi_vals[s])

    if d == 1:
        v = [ [0 for t in phi_vals] ]
    else:
        v = basis_values(invars, phi_vals, s, d-1)

    if d == len(phi_vals[s]):
        return v + [phi_vals[s][d-1]]
    else:
        bv = [ ]
        t = invars['types'][s][d-1]
        for i in range(0, t['e']*t['f']):
            bv.extend([ [ frac2rat(phi_vals[s][d-1][r]*i + vv[r]) for r in range(0, len(vv)) ] for vv in v ])
        return bv

def basis_indices(tt):
    ind = [ [] ]
    for i in range(0, len(tt)-1):
        nind = [ ]
        for s in range(0, tt[i]['e']*tt[i]['f']):
            for dni in ind:
                nind.append([s] + dni)
        ind = nind

    return [ [0]+i for i in ind ] + [ [1] + [0 for i in range(1, len(tt))] ]

def stepping_alg(bases_vals):
    bvs = [ list(bv) for bv in bases_vals ]

    

    inf = rat(int(math.ceil(sum([ sum([sum(v) for v in bv]) for bv in bvs ]))), 1)
    for s in range(0, len(bvs)):
        bvs[s][len(bvs[s])-1][s] = inf

    J = [ 0 for bv in bvs ]
    ind = [ list(J) ]
    vals = [ ]
    n = sum([len(bv) for bv in bvs])-len(bvs)

    for i in range(0, n):
        S = [ frac2rat(sum([bvs[s][J[s]][r] for s in range(0, len(bvs))])) for r in range(0, len(bvs)) ]
        vals.append(S)
        k = S.index(min(S))
        J[k] += 1


        if sum(J) < n:
            ind.append(list(J))
    
    return ind, vals

def stepping_alg_2(bvp, bvq):
    obvp = list(bvp)
    obvq = list(bvq)

    inf = rat(int(math.ceil(sum([v[0]+v[1] for v in bvp+bvq]))), 1)
    bvp[len(bvp)-1][0] = inf
    bvq[len(bvq)-1][1] = inf

    J = [0, 0]
    ind = [ list(J) ]
    vals = [ ]

    for i in range(0, len(bvp)+len(bvq)-2-1):
        S = [ bvp[J[0]][0]+bvq[J[1]][0], bvp[J[0]][1]+bvq[J[1]][1] ]
        vals.append(S)
        if S[0] <= S[1]:
            J[0] += 1
        else:
            J[1] += 1

        ind.append(list(J))
    S = [ bvp[J[0]][0]+bvq[J[1]][0], bvp[J[0]][1]+bvq[J[1]][1] ]
    vals.append(S)

    return ind, vals

def draw_bases(bvp, bvq, ind, vals, indp, indq, invp, invq, hidden, j):

    size = (600, max(len(bvp), len(bvq))*100 + 200)
    im = Image.new("RGBA", size, (255, 255, 255, 255))
    draw = ImageDraw.Draw(im)
    dr = 4
    pcol = 200
    qcol = 400
    sty = 180
    font = ImageFont.truetype('/Library/Fonts/Verdana.ttf', 12)
    bfont = ImageFont.truetype('./CloisterBlack.ttf', 34)

    (w, h) = draw.textsize("p", font=bfont)
    draw.text((pcol-(w/2), 20), "p", fill="black", font=bfont)
    
    (w, h) = draw.textsize("q", font=bfont)
    draw.text((qcol-(w/2), 20), "q", fill="black", font=bfont)
   
    label = "j = %d" % (j,)
    (w, h) = draw.textsize(label, font=font)
    draw.text((300-(w/2), 80), label, fill="gray", font=font)
    

    if hidden[0] == rat(invp[2][j-1], invp[0][j-1]):
        philab = u"no refinement, "
    else:
        philab = u"refinement, "
    draw.text((pcol-40, 80), "e = %s" %(str(invp[0]),), fill="gray", font=font)
    draw.text((pcol-40, 100), "f = %s" %(str(invp[1]),), fill="gray", font=font)
    draw.text((pcol-40, 120), "h = %s" %(str(invp[2]),), fill="gray", font=font)
    draw.text((pcol-40, 140), philab + u"\u03BB = %s" %(unicode(hidden[0])), fill="gray", font=font)

    if hidden[1] == rat(invq[2][j-1], invq[0][j-1]):
        philab = u"no refinement, "
    else:
        philab = u"refinement, "
    draw.text((qcol-40, 80), "e = %s" %(str(invq[0]),), fill="gray", font=font)
    draw.text((qcol-40, 100), "f = %s" %(str(invq[1]),), fill="gray", font=font)
    draw.text((qcol-40, 120), "h = %s" %(str(invq[2]),), fill="gray", font=font)
    draw.text((qcol-40, 140), philab + u"\u03BB = %s" %(unicode(hidden[1])), fill="gray", font=font)

    bvp[-1][0] = u"\u221E"
    bvq[-1][1] = u"\u221E"
    x, y = (pcol, sty)
    for i in range(0, len(bvp)):
        v = bvp[i]
        draw.ellipse((x-dr, y-dr, x+dr, y+dr), fill="black")

        label = "(%s, %s)" % (unicode(v[0]), unicode(v[1]))
        (w, h) = draw.textsize(label, font=font)
        draw.text((x-w-20, y-(h/2)-1), label, fill="black", font=font)

        label = "("+(', '.join([str(m) for m in indp[i]]))+")"
        (w2, h2) = draw.textsize(label, font=font)
        draw.text((x-w-20-w2-20, y-(h/2)-1), label, fill="gray", font=font)
        
        y += 100

    x, y = (qcol, sty)
    for i in range(0, len(bvq)):
        v = bvq[i]
        draw.ellipse((x-dr, y-dr, x+dr, y+dr), fill="black")
        
        label = "(%s, %s)" % (unicode(v[0]), unicode(v[1]))
        (w, h) = draw.textsize(label, font=font)
        draw.text((x+20, y-(h/2)-1), label, fill="black", font=font)
        
        label = "("+(', '.join([str(m) for m in indq[i]]))+")"
        (w2, h2) = draw.textsize(label, font=font)
        draw.text((x+w+20+20, y-(h/2)-1), label, fill="gray", font=font)

        y += 100

    draw.line((pcol, sty, qcol, sty), width=2, fill="green")
    lasti = [0, 0]
    lastpos = (pcol, sty)
    for i in range(0, len(ind)):
        if i > 0:
            if ind[i][0] != ind[i-1][0]:
                newpos = (pcol, ind[i][0]*100 + sty)
            elif ind[i][1] != ind[i-1][1]:
                newpos = (qcol, ind[i][1]*100 + sty)
            draw.line((lastpos, newpos), width=2, fill="green")
            draw.ellipse((newpos[0]-dr/2, newpos[1]-dr/2, newpos[0]+dr/2, newpos[1]+dr/2), fill="green")
        else:
            newpos = lastpos

        if ind[i][0] >= len(bvp)-1:
            vals[i][0] = u"\u221E"
        if ind[i][1] >= len(bvq)-1:
            vals[i][1] = u"\u221E"
        label = "(%s, %s)" % (unicode(vals[i][0]), unicode(vals[i][1]))
        (w, h) = draw.textsize(label, font=font)
        if newpos[0] == pcol:
            draw.text((newpos[0]-w-20, newpos[1]+(h/2)+4), label, fill="blue", font=font)
        else:
            draw.text((newpos[0]+20, newpos[1]+(h/2)+4), label, fill="blue", font=font)

        lastpos = newpos


    #im.save('/Users/hds/Desktop/tests.png', 'PNG')
    return im

def fetch_j(invars, t1i, t2i):
    if t1i == t2i:
        return len(invars['types'][t1i])
    elif t1i > t2i:
        t1i, t2i = t2i, t1i
    return invars['j'][t1i][t2i-t1i-1]

def fetch_hidden(invars, t1i, t2i):
    return [ invars['hidden'][t1i][t2i], invars['hidden'][t2i][t1i] ]

def set_hidden(invars):
    for i in range(0, len(invars['hidden'])):
        for k in range(0, len(invars['hidden'])):
            if i == k:
                continue
            elif invars['hidden'][i][k] == 0:
                t = invars['types'][i][fetch_j(invars, i, k)-1]
                invars['hidden'][i][k] = rat(t['h'], t['e'])

def inv_article():
    invars = {
        'j': [ [1] ],
        'hidden': [ [0, 0,],
                    [0, 0],
                  ],
        'types': [
            [ {'e': 3, 'f': 2, 'h': 2},
              {'e': 1, 'f': 1, 'h': 6}, ],
            [ {'e': 3, 'f': 1, 'h': 1},
              {'e': 2, 'f': 1, 'h': 9},
              {'e': 1, 'f': 1, 'h': 12}, ],
        ],
    }

    return invars

def inv_article_3():
    invars = {
        'j': [ [1,1],
               [1,],
             ],
        'hidden': [ [0, 0, 0],
                    [0, 0, 0],
                    [0, 0, 0],
                  ],
        'types': [
            [ {'e': 3, 'f': 2, 'h': 2},
              {'e': 1, 'f': 1, 'h': 6}, ],
            [ {'e': 3, 'f': 1, 'h': 2},
              {'e': 2, 'f': 1, 'h': 9},
              {'e': 1, 'f': 1, 'h': 12}, ],
            [ {'e': 2, 'f': 1, 'h': 1},
              {'e': 3, 'f': 1, 'h': 9},
              {'e': 1, 'f': 1, 'h': 12}, ],
        ],
    }

    return invars

def inv_break():
    pe = [1, 1, 1, 1]
    pf = [3, 2, 2, 1]
    ph = [1, 5, 4, 5]

    qe = [1, 1, 1, 1]
    qf = [3, 3, 2, 1]
    qh = [1, 1, 4, 12]

    j = 2
    hidden = [0, 0]

    return pe, pf, ph, qe, qf, qh, j, hidden

def inv_break_j1():
    pe = [1, 1, 1]
    pf = [3, 2, 1]
    ph = [5, 4, 5]

    qe = [1, 1, 1]
    qf = [3, 2, 1]
    qh = [2, 3, 12]

    j = 1
    hidden = [0, 1]

    return pe, pf, ph, qe, qf, qh, j, hidden

def changed_index(l1, l2):
    if len(l1) != len(l2):
        return -1
    for i in range(0, len(l1)):
        if l1[i] != l2[i]:
            return i
    return -1

#pe, pf, ph, qe, qf, qh, j, hidden = inv_article()
#pe, pf, ph, qe, qf, qh, j, hidden = inv_break()
#pe, pf, ph, qe, qf, qh, j, hidden = inv_break_j1()

def stepping_invariants(invars):
    #invars = inv_article_3()
    set_hidden(invars)

    phi_vals = phi_values(invars)

    bases_vals = [ basis_values(invars, phi_vals, s, 0) for s in range(0, len(phi_vals)) ]

    bases_inds = [ basis_indices(tt) for tt in invars['types'] ]

    ind, vals = stepping_alg(bases_vals)

    results = {
        'phi_vals': phi_vals,
        'bases_vals': bases_vals,
        'bases_inds': bases_inds,
        'values': vals,
        'indices': ind,
        'ind_delta': [0] + [ changed_index(ind[i-1], ind[i]) for i in range(1, len(ind)) ],
        'count': len(phi_vals),
        'n': len(ind),
        'ns': [ len(i) for i in bases_inds ]
    }
    results.update(invars)
     
    return json.dumps(results, cls=SteppingJSONEncoder)


# invars = inv_article_3()
# set_hidden(invars)
# 
# print invars
# 
# phi_vals = phi_values(invars)
# print phi_vals
# 
# bases_vals = [ basis_values(invars, phi_vals, s, 0) for s in range(0, len(phi_vals)) ]
# print bases_vals
# 
# bases_inds = [ basis_indices(tt) for tt in invars['types'] ]
# print bases_inds
# 
# ind, vals = stepping_alg(bases_vals)
# 
# print ind
# print vals
# 
# results = {
#     'phi_vals': phi_vals,
#     'bases_vals': bases_vals,
#     'bases_inds': bases_inds,
#     'values': vals,
#     'indices': ind,
#     'ind_delta': [0] + [ changed_index(ind[i-1], ind[i]) for i in range(1, len(ind)) ],
#     'count': len(phi_vals),
#     'n': len(ind),
#     'ns': [ len(i) for i in bases_inds ]
# }
# results.update(invars)
#  
# #print json.dumps(['0'])
# print json.dumps(results, cls=SteppingJSONEncoder)
# 
# 
# quit()

##  
##  #phip, phiq = phi_values(pe, pf, ph, qe, qf, qh, j, hidden)
##  
##  #print phip
##  #print phiq
##  
##  bvp = basis_values(pe, pf, phip, 0)
##  bvq = basis_values(qe, qf, phiq, 0)
##  indp = basis_ind(pe, pf)
##  indq =  basis_ind(qe, qf)
##  
##  #print ""
##  #print bvp
##  #print bvq
##  
##  ind, vals = stepping_alg(bvp, bvq)
##  invp = [pe, pf, ph]
##  invq = [qe, qf, qh]
##  
##  im = draw_bases(bvp, bvq, ind, vals, indp, indq, invp, invq, hidden, j)
##  
##  
##  
##  filename = '/Users/hds/Desktop/test.png'
##  if len(sys.argv) > 1:
##      filename = sys.argv[1]
##  im.save(filename, 'PNG')
