import sys
import re

import fractions
import math
import operator
from operator import mul
from random import choice
import numbers
import json
from json.encoder import JSONEncoder
from itertools import product, combinations
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

def str2rat(s):
    if '/' in s:
        (num, denom) = s.split('/')
        return rat(int(num), int(denom))
    else:
        return rat(int(s), 1)

def prod(l):
    return reduce(mul, l, 1)

def V_i(tt, i):
    if i == 1:
        return 0
    else:
        i -= 1
        return tt[i-1]['e'] * tt[i-1]['f'] * (tt[i-1]['e'] * V_i(tt, i) + tt[i-1]['h'])

def n_p(tt):
    return prod([t['e']*t['f'] for t in tt])

def total_degree(types):
    return sum([n_p(tt) for tt in types])

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

    #print tt
    #print [ [0]+i for i in ind ] + [ [1] + [0 for i in range(1, len(tt))] ]
    return [ [0]+i for i in ind ] + [ [1] + [0 for i in range(1, len(tt))] ]

def brute_force_alg(bases_vals):
    bvs = [ list(bv) for bv in bases_vals ];

    inf = rat(int(math.ceil(sum([ sum([sum(v) for v in bv]) for bv in bvs ]))), 1)
    for s in range(0, len(bvs)):
        bvs[s][len(bvs[s])-1][s] = inf

    J = [ 0 for bv in bvs ]
    n = sum([len(bv) for bv in bvs])-len(bvs)

    #print bvs

    ind = [ [] for m in range(0, n) ]
    vals = [ [] for m in range(0, n) ]
    for i in range(0, reduce(mul, [len(bv) for bv in bvs])):
        j = 0
        for j in range(0, len(J)):
            J[j] = i % len(bvs[j])
            i = (i - J[j]) / len(bvs[j])
        
        m = sum(J)
        S = [ frac2rat(sum([bvs[s][J[s]][r] for s in range(0, len(bvs))])) for r in range(0, len(bvs)) ]

        if sum(J) < n:
            vals[m].append(S)
            ind[m].append(list(J))

    return ind, vals

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

def make_hidden_for_triple(inv, triple):
    hidden = [['-' for i in triple] for j in triple]
    for i in range(0, len(triple)):
        for j in range(0, len(triple)):
            hidden[i][j] = inv['hidden'][triple[i]][triple[j]]

    return hidden

def verify_inv(inv):
    
    hslopes = inv['hidden']
    types = inv['types']

    tcount = len(inv['types'])
    for s in range(0, tcount):
        for t in range(s+1, tcount):
            j = fetch_j(inv, s, t)
            if j == 0:
                raise ValueError("index of coincidence cannot be 0, this is a single tree")
            if j > len(types[s]):
                raise ValueError("index of coincidence cannot be greater than %(r)d for t_%(s)d" % {'r': len(types[s]), 's': s+1})
            if j > len(types[t]):
                raise ValueError("index of coincidence cannot be greater than %(r)d for t_%(s)d" % {'r': len(types[s]), 't':t+1})
            for i in range(0, j-1):
                for var in ['e', 'f', 'h']:
                    if types[s][i][var] != types[t][i][var]:
                        raise ValueError("%(var)s_%(level)d does not match for t_%(s)d and t_%(t)d below index of coincidence j = %(j)d" % {
                            'var': var,
                            'level': i+1,
                            's': s+1,
                            't': t+1,
                            'j': j })

    for s in range(0, len(types)):
        for i in range(0, len(types[s])-1):
            if types[s][i]['e']*types[s][i]['f'] == 1:
                raise ValueError("e_%(level)d * f_%(level)d = 1 in t_%(s)d" % {'level': i+1, 's': s+1})
            if fractions.gcd(types[s][i]['h'], types[s][i]['e']) != 1:
                raise ValueError("h_%(level)d and e_%(level)d are not relatively prime in t_%(s)d" % {'level': i+1, 's': s+1})


    for s in range(0, tcount):
        for t in range(0, tcount):
            if s == t:
                continue

            lam_st, lam_ts = fetch_hidden(inv, s, t, or_slope=False)
            j = fetch_j(inv, s, t)
            if lam_st > 0:
                if lam_st != int(lam_st):
                    print lam_st
                    raise ValueError("cutting slope lambda_{p_%(s)d}^{p_%(t)d} not an integer" % {'s': s+1, 't': t+1})
                if lam_st > rat(types[s][j-1]['h'], types[s][j-1]['e']):
                    raise ValueError("cutting slope lambda_{p_%(s)d}^{p_%(t)d} greater than h_%(j)d/e_%(j)d" % {'s': s+1, 't': t+1, 'j': j})

    for s, t, u in combinations(range(0, tcount), 3):
        if fetch_j(inv, s, t) == fetch_j(inv, s, u) == fetch_j(inv, t, u):
            hidden = make_hidden_for_triple(inv, [s, t, u])
            if hidden[0][1] == hidden[0][2] and hidden[2][0] == hidden[2][1] \
                    and hidden[1][0] == hidden[1][2]:
                pass
            elif hidden[0][1] == hidden[0][2] and hidden[1][0] == hidden[2][0] \
                    and hidden[1][0] > 0 \
                    and hidden[1][0] < hidden[1][2] \
                    and hidden[2][0] < hidden[2][1]:
                pass
            elif hidden[0][2] == hidden[1][2] and hidden[2][0] == hidden[2][1] \
                    and hidden[0][2] > 0 \
                    and hidden[0][2] < hidden[0][1] \
                    and hidden[1][2] < hidden[1][0]:
                pass
            else:
                raise ValueError("hidden values are not valid for triple (t_%(s)d, t_%(t)d, t_%(u)d)" % ({'s': s+1, 't': t+1, 'u': u+1})) 

    return True
    
#def level_from_sequence(seq):
#    return {'e': seq.pop(0), 'f': seq.pop(0), 'h': seq.pop(0)}

def types_from_sequence(r, seq):
    
    if sum(r) != len(seq):
        raise ValueError("sequence not the correct length")

    types = [ ]
    v = ('e', 'f', 'h')
    for r_s in r:
        types.append([dict(zip(v, seq.pop(0))) for i in range(0, r_s)])

    valid = True
    for lvl in [lvl for levels in types for lvl in levels[:-1]]:
        if lvl['e']*lvl['f'] == 1:
            valid = False
        if fractions.gcd(lvl['h'], lvl['e']) != 1:
            valid = False

    if valid:
        return types
    else:
        return False

def basic_indco_from_r(r):
    indco = [ ]
    for s in range(0, len(r)-1):
        indco.append([])
        for t in range(s+1, len(r)):
            indco[-1].append(1)

    return indco

def all_indco_for_r(r):
    pools = [ ]
    for s in range(0, len(r)-1):
        for t in range(s+1, len(r)):
            max_indco = min([r[s], r[t]])
            pools.append(range(1, max_indco))

    all_indco = [ ]
    for seq in product(*pools):
        seq = list(seq)
        valid = True
        indco = [ ]
        for s in range(0, len(r)-1):
            indco.append([])
            for t in range(s+1, len(r)):
                if t > s+1 and seq[0] > indco[-1][-1]:
                    valid = False
                elif s > 0:
                    if seq[0] < indco[s-1][t-(s-1)-1]:
                        valid = False
                    elif indco[s-1][s-(s-1)-1] != indco[s-1][t-(s-1)-1] and seq[0] != min(indco[s-1][s-(s-1)-1], indco[s-1][t-(s-1)-1]):
                        valid = False
                indco[-1].append(seq.pop(0))
        if valid:
            all_indco.append(indco)
    
    return all_indco
   
def valid_indco_for_r_types(r, types):
    tcount = len(types)
    valid_indco = [ ]
    for indco in all_indco_for_r(r):
        if indco_valid_for_types(indco, types):
            valid_indco.append(indco)

    return valid_indco

def indco_valid_for_types(indco, types):
    tcount = len(types)
    for s in range(0, tcount):
        for t in range(s+1, tcount):
            j = fetch_j({'j': indco}, s, t)
            for i in range(0, j-1):
                for var in ['e', 'f', 'h']:
                    if types[s][i][var] != types[t][i][var]:
#                        print "%(var)s_%(level)d does not match for t_%(s)d and t_%(t)d below index of coincidence j = %(j)d" % {
#                            'var': var,
#                            'level': i+1,
#                            's': s+1,
#                            't': t+1,
#                            'j': j }
                        return False
    return True

def basic_hidden_from_r(r):
    return [ [0 for s in range(0, len(r))] for t in range(0, len(r)) ]

def all_hidden_for_types_indco(types, indco):
    tcount = len(types)

    pools = [ ]
    for s in range(0, tcount):
        for t in range(0, tcount):
            if s == t:
                pools.append([0])
            else:
                j = fetch_j({'j': indco}, s, t)
                slope = rat(types[s][j-1]['h'], types[s][j-1]['e'])
                pools.append([0] + [i for i in range(1, int(math.ceil(slope)))])

    all_hidden = [ ]
    for seq in product(*pools):
        hidden = [list(seq[i:i+tcount]) for i in range(0, tcount*tcount, tcount)]
        all_hidden.append(hidden)

    return all_hidden

def generate_sequences(random=0):
    r = [3, 3, 3]
    okutsu_range = [1, 2, 3, 4]
    o_vars = okutsu_vars(okutsu_range)
    o_vars.sort(key=lambda v: v[2], reverse=True)

    if random > 0:
        generate_random_sequences_for_r(r, o_vars, okutsu_range, count=random)
    else:
        generate_sequences_for_r(r, o_vars, okutsu_range)

def okutsu_vars(okutsu_range):
    okutsu_vars = []
    for lvl in product(okutsu_range, okutsu_range, okutsu_range):
        e, f, h = lvl
        if e*f > 1 and fractions.gcd(h, e) == 1:
            okutsu_vars.append(list(lvl))
    return okutsu_vars

def test_single():
    r = [2, 3, 2]
    types = [[{"h": 4, "e": 3, "f": 4}, {"h": 3, "e": 1, "f": 1}], [{"h": 4, "e": 1, "f": 2}, {"h": 1, "e": 2, "f": 4}, {"h": 4, "e": 1, "f": 1}], [{"h": 4, "e": 3, "f": 4}, {"h": 1, "e": 1, "f": 1}]]
    types = [[{"h": 4, "e": 1, "f": 3}, {"h": 1, "e": 1, "f": 1}], [{"h": 4, "e": 1, "f": 3}, {"h": 4, "e": 1, "f": 4}, {"h": 2, "e": 1, "f": 1}], [{"h": 3, "e": 1, "f": 3}, {"h": 2, "e": 1, "f": 1}]]
    r = [3, 3, 3]
    types = [[{"h": 1, "e": 1, "f": 4}, {"h": 1, "e": 1, "f": 2}, {"h": 2, "e": 1, "f": 1}], [{"h": 1, "e": 2, "f": 2}, {"h": 3, "e": 4, "f": 1}, {"h": 2, "e": 1, "f": 1}], [{"h": 2, "e": 1, "f": 3}, {"h": 4, "e": 1, "f": 3}, {"h": 3, "e": 1, "f": 1}]]

    tpassed, tfailed, tskipped = test_all_for_types(r, types)
    print "\nTotal Passed: %d\nTotal Failed: %d\nTotal Skipped: %d" % (
            tpassed, tfailed, tskipped,)


def generate_random_sequences_for_r(r, okutsu_vars, hs, count=100):
   
    tpassed, tfailed, tskipped = (0, 0, 0)
    for test in range(0, count):
        seq = []
        for r_s in r:
            seq += [list(choice(okutsu_vars)) for i in range(0, r_s-1)]
            seq.append([1, 1, choice(hs)])
        
        types = types_from_sequence(r, list(seq))
        if types is False:
            continue

        passed, failed, skipped = test_all_for_types(r,
                                                     types,
                                                     name="Test %d" % (test,))
        tpassed += passed
        tfailed += failed
        tskipped += skipped

    print "\nTotal Passed: %d\nTotal Failed: %d\nTotal Skipped: %d" % (
            tpassed, tfailed, tskipped,)

def test_all_for_types(r, types, name="Test"):
    tpassed, tfailed, tskipped = (0, 0, 0)

    print "\n--=== %s (n = %d) ===--" % (name, total_degree(types))
    print "\"r\": %s" % (json.dumps(r, cls=SteppingJSONEncoder),)
    print "\"types\": %s" % (json.dumps(types, cls=SteppingJSONEncoder),)
    #all_indco = all_indco_for_r(r)
    all_indco = valid_indco_for_r_types(r, types)
    for indco in all_indco:
        all_hidden = all_hidden_for_types_indco(types, indco)
        #print "Hidden slope combinations: %d" % (len(all_hidden),)
        passed = 0
        failed = 0
        skipped = 0
        for hidden in all_hidden:
            inv = {
                'j': indco,
                'hidden': hidden,
                'types': types,
            }

            try:
                verify_inv(inv)
            except ValueError, e:
                skipped += 1
                print "Skipped (%s): %s" % (str(e), str(hidden),)
                continue
                
            if stepping_vs_brute_force(inv) is True:
                passed += 1
                #print "Pass"
                pass
            else:
                failed += 1
                print "FAIL: %s" % (json.dumps(inv, cls=SteppingJSONEncoder),)
#                    if failed > 4:
#                        print "Lots failed, skipping remainder of tests."
#                        break
        print "    P: %d, F: %d, S: %d    %s" % (
                passed, failed, skipped,
                json.dumps(indco, cls=SteppingJSONEncoder))
        tpassed += passed
        tfailed += failed
        tskipped += skipped

    return tpassed, tfailed, tskipped


def generate_sequences_for_r(r, okutsu_vars, hs):
    #r = [3, 2]
    seq = [3, 2, 2, 1, 1, 6, 3, 1, 1, 2, 1, 9, 1, 1, 12]
    
    pools = []
    for r_s in r:
        pools += [list(okutsu_vars) for i in range(0, r_s-1)]
        pools.append([list(p) for p in product([1], [1], hs)])
    #print pools
    #pools = [list(okutsu_vars) for i in range(0, sum(r))]

    total = 0
    valid = 0
    combinations = []
    
    seqs = 0
    
    all_indco = all_indco_for_r(r)
    okutsu_combs = prod([len(p) for p in pools])
    print "Okutsu combinations per level: %d" % (len(okutsu_vars),)
    print "Okutsu total combinations: %d" % (okutsu_combs,)
    print "Index of coincidense combinations: %d" % (len(all_indco),)

    for seq in product(*pools):
        seq = list(seq)
        types = types_from_sequence(r, list(seq))
        
        if types is False:
            continue

        for indco in all_indco:
            all_hidden = all_hidden_for_types_indco(types, indco)
            if total == 0:
                print "Max hidden slope combinations: %d" % (len(all_hidden),)
                print "Max total combinations: %d" % (len(all_hidden)*len(all_indco)*okutsu_combs,)
            for hidden in all_hidden:
                inv = {
                    'j': indco,
                    'hidden': hidden,
                    'types': types,
                }

                total += 1
                try:
                    verify_inv(inv)
                except ValueError, e:
                    continue
                
                if re.match(r'^[1-9][0]+$', str(valid)):
                    print "Prepared: %d" % (valid,)
                
                combinations.append(inv)
                valid += 1

    print "Testing combinations: %d / %d" % (valid, total,)

    for i in range(0, valid):
        if stepping_vs_brute_force(combinations[i]) is True:
            pass
            #print "True!"
        else:
            print "False!"
            print inv

        if int((i+1)*100/float(valid)) > int((i)*100/float(valid)):
            print "Checked: %d%%" % (int((i+1)*100/float(valid)),)


def fetch_j(invars, t1i, t2i):
    if t1i == t2i:
        return len(invars['types'][t1i])
    elif t1i > t2i:
        t1i, t2i = t2i, t1i
    return invars['j'][t1i][t2i-t1i-1]

def hidden_or_slope(invars, t1i, t2i):
    if isinstance(invars['hidden'][t1i][t2i], basestring):
        return str2rat(invars['hidden'][t1i][t2i])
    elif invars['hidden'][t1i][t2i] == 0:
        t = invars['types'][t1i][fetch_j(invars, t1i, t2i)-1]
        return rat(t['h'], t['e'])
    else:
        return invars['hidden'][t1i][t2i]

def fetch_hidden(invars, t1i, t2i, or_slope=True):
    if or_slope is True:
        return [ hidden_or_slope(invars, t1i, t2i), hidden_or_slope(invars, t2i, t1i) ]
    else:
        return [ invars['hidden'][t1i][t2i], invars['hidden'][t2i][t1i] ]

def set_hidden(invars):
    for i in range(0, len(invars['hidden'])):
        for k in range(0, len(invars['hidden'])):
            if i == k:
                continue
            elif isinstance(invars['hidden'][i][k], basestring):
                invars['hidden'][i][k] = str2rat(invars['hidden'][i][k])
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

def inv_article_invalid():
    invars = {
        'j': [ [1] ],
        'hidden': [ [0, 1,],
                    [1, 0],
                  ],
        'types': [
            [ {'e': 3, 'f': 2, 'h': 4},
              {'e': 2, 'f': 1, 'h': 7},
              {'e': 1, 'f': 1, 'h': 6}, ],
            [ {'e': 3, 'f': 1, 'h': 8},
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

def compare_results(ind1, vals1, ind2, vals2, printvals=False):
    n = len(ind1)
    correct = True

    if printvals:
        print "\nStepping vs Brute:"
    for m in range(0, n):
        minvals = [ min(v) for v in vals2[m] ]
        val = max(minvals)
        i = minvals.index(val)
        if val == min(vals1[m]):
            if printvals:
                print "%d: %s --> |_ %s _| = %d  ==  %d = |_ %s _| <-- %s  TRUE" % (
                        m, str(ind2[m][i]), str(val), math.floor(val),
                        math.floor(min(vals1[m])), min(vals1[m]), str(ind1[m]))
        else:
            correct = False
            if printvals:
                print "%d: %s --> |_ %s _| = %d  ==  %d = |_ %s _| <-- %s  !! FALSE !!" % (
                        m, str(ind2[m][i]), str(val), math.floor(val),
                        math.floor(min(vals1[m])), min(vals1[m]), str(ind1[m]))
                for i in range(0, len(ind2[m])):
                    print "  %s: %s" % (str(ind2[m][i]), str(vals2[m][i]),)

    return correct


def print_stepping_vs_brute(ind, vals, bind, bvals):
    n = len(ind)
    correct = True
    output = ''
    
    output += "Stepping vs Brute:\n"
    for m in range(0, n):
        minvals = [ min(v) for v in bvals[m] ]
        val = max(minvals)
        i = minvals.index(val)
        if val == min(vals[m]):
            output += "%d: %s --> |_ %s _| = %d  ==  %d = |_ %s _| <-- %s  TRUE\n" % (m, str(bind[m][i]), str(val), math.floor(val), math.floor(min(vals[m])), min(vals[m]), str(ind[m]))
        else:
            correct = False
            output += "%d: %s --> |_ %s _| = %d  ==  %d = |_ %s _| <-- %s  !! FALSE !!\n" % (m, str(bind[m][i]), str(val), math.floor(val), math.floor(min(vals[m])), min(vals[m]), str(ind[m]))
            for i in range(0, len(bind[m])):
                output += "  %s: %s\n" % (str(bind[m][i]), str(bvals[m][i]),)

    return correct, output

def stepping_vs_brute_force(inv):
    #set_hidden(inv)

    phi_vals = phi_values(inv)

    bases_vals = [ basis_values(inv, phi_vals, s, 0) for s in range(0, len(phi_vals)) ]
    bases_vals_diff = [ ]
    for s in range(0, len(phi_vals)):
        vals = [ bases_vals[s][0] ]
        vals.extend([ [ Rat(bases_vals[s][m][i] - bases_vals[s][m-1][i]) for i in range(0, len(bases_vals[s][m])) ] for m in range(1, len(bases_vals[s])) ])
        bases_vals_diff.append(vals)

    bases_inds = [ basis_indices(tt) for tt in inv['types'] ]

    st_ind, st_vals = stepping_alg(bases_vals)
    bf_ind, bf_vals = brute_force_alg(bases_vals)

    correct = compare_results(st_ind, st_vals, bf_ind, bf_vals)

    return correct


def stepping_invariants(invars):
    #invars = inv_article_3()

    valid = True
    error = None
    try:
        verify_inv(invars)
    except ValueError, e:
        print "INVALID:", e
        valid = False
        error = str(e)
    set_hidden(invars)

    phi_vals = phi_values(invars)

    bases_vals = [ basis_values(invars, phi_vals, s, 0) for s in range(0, len(phi_vals)) ]
    bases_vals_diff = [ ]
    for s in range(0, len(phi_vals)):
        vals = [ bases_vals[s][0] ]
        vals.extend([ [ Rat(bases_vals[s][m][i] - bases_vals[s][m-1][i]) for i in range(0, len(bases_vals[s][m])) ] for m in range(1, len(bases_vals[s])) ])
        bases_vals_diff.append(vals)

    bases_inds = [ basis_indices(tt) for tt in invars['types'] ]

    bind, bvals = brute_force_alg(bases_vals)
    ind, vals = stepping_alg(bases_vals)

    results = {
        'phi_vals': phi_vals,
        'bases_vals': bases_vals,
        'bases_vals_diff': bases_vals_diff,
        'bases_inds': bases_inds,
        'values': vals,
        'indices': ind,
        'ind_delta': [0] + [ changed_index(ind[i-1], ind[i]) for i in range(1, len(ind)) ],
        'count': len(phi_vals),
        'n': len(ind),
        'ns': [ len(i) for i in bases_inds ],
        'valid': valid,
    }
    results.update(invars)
    
    correct, output = print_stepping_vs_brute(ind, vals, bind, bvals)
    if correct is False:
        if error is None:
            error = 'Stepping algorithm failed!'
    results.update({'error': error, 'correct': correct, 'vs_log': output})
    
    
    return json.dumps(results, cls=SteppingJSONEncoder)

if __name__=="__main__":
    test_single()
    #generate_sequences(random=100)

    #print stepping_invariants(inv_article()) 

