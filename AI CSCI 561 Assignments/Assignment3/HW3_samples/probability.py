"""Probability models. (Chapter 13-15)
"""
import random

def extend(s, var, val):
    s2 = s.copy()
    s2[var] = val
    return s2

def update(x, **entries):
    #Update a dict; or an object with slots; according to entries.
    if isinstance(x, dict):
        x.update(entries)
    else:
        x.__dict__.update(entries)
    return x


class DefaultDict(dict):
    """Dictionary with a default value for unknown keys."""
    def __init__(self, default):
        self.default = default

    def __getitem__(self, key):
        if key in self: return self.get(key)
        return self.setdefault(key, copy.deepcopy(self.default))

    def __copy__(self):
        copy = DefaultDict(self.default)
        copy.update(self)
        return copy


def every(predicate, seq):
    """True if every element of seq satisfies predicate.
    >>> every(callable, [min, max])
    1
    >>> every(callable, [min, 3])
    0
    """
    for x in seq:
        if not predicate(x): return False
    return True


def probability(p):
    "Return true with probability p."
    return p > random.uniform(0.0, 1.0)



def if_(test, result, alternative):
    """Like C++ and Java's (test ? result : alternative), except
    both result and alternative are always evaluated. However, if
    either evaluates to a function, it is applied to the empty arglist,
    so you can delay execution by putting it in a lambda.
    >>> if_(2 + 2 == 4, 'ok', lambda: expensive_computation())
    'ok'
    """
    if test:
        if callable(result): return result()
        return result
    else:
        if callable(alternative): return alternative()
        return alternative

#______________________________________________________________________________

def DTAgentProgram(belief_state):
    "A decision-theoretic agent. [Fig. 13.1]"
    def program(percept):
        belief_state.observe(program.action, percept)
        program.action = argmax(belief_state.actions(),
                                belief_state.expected_outcome_utility)
        return program.action
    program.action = None
    return program

#______________________________________________________________________________

class ProbDist:
    """A discrete probability distribution.  You name the random variable
    in the constructor, then assign and query probability of values.
    >>> P = ProbDist('Flip'); P['H'], P['T'] = 0.25, 0.75; P['H']
    0.25
    >>> P = ProbDist('X', {'lo': 125, 'med': 375, 'hi': 500})
    >>> P['lo'], P['med'], P['hi']
    (0.125, 0.375, 0.5)
    """
    def __init__(self, varname='?', freqs=None):
        """If freqs is given, it is a dictionary of value: frequency pairs,
        and the ProbDist then is normalized."""
        update(self, prob={}, varname=varname, values=[])
        if freqs:
            for (v, p) in freqs.items():
                self[v] = p
            self.normalize()

    def __getitem__(self, val):
        "Given a value, return P(value)."
        try: return self.prob[val]
        except KeyError: return 0

    def __setitem__(self, val, p):
        "Set P(val) = p."
        if val not in self.values:
            self.values.append(val)
        self.prob[val] = p

    def normalize(self):
        """Make sure the probabilities of all values sum to 1.
        Returns the normalized distribution.
        Raises a ZeroDivisionError if the sum of the values is 0.
        >>> P = ProbDist('Flip'); P['H'], P['T'] = 35, 65
        >>> P = P.normalize()
        >>> print '%5.3f %5.3f' % (P.prob['H'], P.prob['T'])
        0.350 0.650
        """
        total = float(sum(self.prob.values()))
        if not (1.0-epsilon < total < 1.0+epsilon):
            for val in self.prob:
                self.prob[val] /= total
        return self

    def show_approx(self, numfmt='%.3g'):
        """Show the probabilities rounded and sorted by key, for the
        sake of portable doctests."""
        return ', '.join([('%s: ' + numfmt) % (v, p)
                          for (v, p) in sorted(self.prob.items())])

epsilon = 0.001

class JointProbDist(ProbDist):
    """A discrete probability distribute over a set of variables.
    >>> P = JointProbDist(['X', 'Y']); P[1, 1] = 0.25
    >>> P[1, 1]
    0.25
    >>> P[dict(X=0, Y=1)] = 0.5
    >>> P[dict(X=0, Y=1)]
    0.5"""
    def __init__(self, variables):
        update(self, prob={}, variables=variables, vals=DefaultDict([]))

    def __getitem__(self, values):
        "Given a tuple or dict of values, return P(values)."
        values = event_values(values, self.variables)
        return ProbDist.__getitem__(self, values)

    def __setitem__(self, values, p):
        """Set P(values) = p.  Values can be a tuple or a dict; it must
        have a value for each of the variables in the joint. Also keep track
        of the values we have seen so far for each variable."""
        values = event_values(values, self.variables)
        self.prob[values] = p
        for var, val in zip(self.variables, values):
            if val not in self.vals[var]:
                self.vals[var].append(val)

    def values(self, var):
        "Return the set of possible values for a variable."
        return self.vals[var]

    def __repr__(self):
        return "P(%s)" % self.variables

def event_values(event, vars):
    """Return a tuple of the values of variables vars in event.
    >>> event_values ({'A': 10, 'B': 9, 'C': 8}, ['C', 'A'])
    (8, 10)
    >>> event_values ((1, 2), ['C', 'A'])
    (1, 2)
    """
    if isinstance(event, tuple) and len(event) == len(vars):
        return event
    else:
        return tuple([event[var] for var in vars])

#______________________________________________________________________________

def enumerate_joint_ask(X, e, P):
    """Return a probability distribution over the values of the variable X,
    given the {var:val} observations e, in the JointProbDist P. [Section 13.3]
    >>> P = JointProbDist(['X', 'Y'])
    >>> P[0,0] = 0.25; P[0,1] = 0.5; P[1,1] = P[2,1] = 0.125
    >>> enumerate_joint_ask('X', dict(Y=1), P).show_approx()
    '0: 0.667, 1: 0.167, 2: 0.167'
    """
    assert X not in e, "Query variable must be distinct from evidence"
    Q = ProbDist(X) # probability distribution for X, initially empty
    Y = [v for v in P.variables if v != X and v not in e] # hidden vars.
    for xi in P.values(X):
        Q[xi] = enumerate_joint(Y, extend(e, X, xi), P)
    return Q.normalize()

def enumerate_joint(vars, e, P):
    """Return the sum of those entries in P consistent with e,
    provided vars is P's remaining variables (the ones not in e)."""
    if not vars:
        return P[e]
    Y, rest = vars[0], vars[1:]
    return sum([enumerate_joint(rest, extend(e, Y, y), P)
                for y in P.values(Y)])

#______________________________________________________________________________

class BayesNet:
    "Bayesian network containing only boolean-variable nodes."

    def __init__(self, node_specs=[]):
        "nodes must be ordered with parents before children."
        update(self, nodes=[], vars=[])
        for node_spec in node_specs:
            self.add(node_spec)

    def add(self, node_spec):
        """Add a node to the net. Its parents must already be in the
        net, and its variable must not."""
        node = BayesNode(*node_spec)
        assert node.variable not in self.vars
        assert every(lambda parent: parent in self.vars, node.parents)
        self.nodes.append(node)
        self.vars.append(node.variable)
        for parent in node.parents:
            self.variable_node(parent).children.append(node)

    def variable_node(self, var):
        """Return the node for the variable named var.
        >>> burglary.variable_node('Burglary').variable
        'Burglary'"""
        for n in self.nodes:
            if n.variable == var:
                return n
        raise Exception("No such variable: %s" % var)

    def variable_values(self, var):
        "Return the domain of var."
        return [True, False]

    def __repr__(self):
        return 'BayesNet(%r)' % self.nodes

class BayesNode:
    """A conditional probability distribution for a boolean variable,
    P(X | parents). Part of a BayesNet."""

    def __init__(self, X, parents, cpt):
        """X is a variable name, and parents a sequence of variable
        names or a space-separated string.  cpt, the conditional
        probability table, takes one of these forms:

        * A number, the unconditional probability P(X=true). You can
          use this form when there are no parents.

        * A dict {v: p, ...}, the conditional probability distribution
          P(X=true | parent=v) = p. When there's just one parent.

        * A dict {(v1, v2, ...): p, ...}, the distribution P(X=true |
          parent1=v1, parent2=v2, ...) = p. Each key must have as many
          values as there are parents. You can use this form always;
          the first two are just conveniences.

        In all cases the probability of X being false is left implicit,
        since it follows from P(X=true).

        >>> X = BayesNode('X', '', 0.2)
        >>> Y = BayesNode('Y', 'P', {T: 0.2, F: 0.7})
        >>> Z = BayesNode('Z', 'P Q',
        ...    {(T, T): 0.2, (T, F): 0.3, (F, T): 0.5, (F, F): 0.7})
        """
        if isinstance(parents, str): parents = parents.split()

        # We store the table always in the third form above.
        if isinstance(cpt, (float, int)): # no parents, 0-tuple
            cpt = {(): cpt}
        elif isinstance(cpt, dict):
            if cpt and isinstance(cpt.keys()[0], bool): # one parent, 1-tuple
                cpt = dict(((v,), p) for v, p in cpt.items())

        assert isinstance(cpt, dict)
        for vs, p in cpt.items():
            assert isinstance(vs, tuple) and len(vs) == len(parents)
            assert every(lambda v: isinstance(v, bool), vs)
            assert 0 <= p <= 1

        update(self, variable=X, parents=parents, cpt=cpt, children=[])

    def p(self, value, event):
        """Return the conditional probability
        P(X=value | parents=parent_values), where parent_values
        are the values of parents in event. (event must assign each
        parent a value.)
        >>> bn = BayesNode('X', 'Burglary', {T: 0.2, F: 0.625})
        >>> bn.p(False, {'Burglary': False, 'Earthquake': True})
        0.375"""
        assert isinstance(value, bool)
        ptrue = self.cpt[event_values(event, self.parents)]
        return if_(value, ptrue, 1 - ptrue)

    def sample(self, event):
        """Sample from the distribution for this variable conditioned
        on event's values for parent_vars. That is, return True/False
        at random according with the conditional probability given the
        parents."""
        return probability(self.p(True, event))

    def __repr__(self):
        return repr((self.variable, ' '.join(self.parents)))

# Burglary example [Fig. 14.2]

T, F = True, False

burglary = BayesNet([
    ('A', '', 1),
    ('B', 'A', {T:0.8,F:0.5}),
    ('C', 'B', {T:0.2,F:0.3}),
    ('B', 'A', {T:0.8,F:0.5})
    ])

#______________________________________________________________________________

def enumeration_ask(X, e, bn):
    """Return the conditional probability distribution of variable X
    given evidence e, from BayesNet bn. [Fig. 14.9]
    >>> enumeration_ask('Burglary', dict(JohnCalls=T, MaryCalls=T), burglary
    ...  ).show_approx()
    'False: 0.716, True: 0.284'"""
    assert X not in e, "Query variable must be distinct from evidence"
    Q = ProbDist(X)
    for xi in bn.variable_values(X):
        Q[xi] = enumerate_all(bn.vars, extend(e, X, xi), bn)
    return Q.normalize()

def enumerate_all(vars, e, bn):
    """Return the sum of those entries in P(vars | e{others})
    consistent with e, where P is the joint distribution represented
    by bn, and e{others} means e restricted to bn's other variables
    (the ones other than vars). Parents must precede children in vars."""
    if not vars:
        return 1.0
    Y, rest = vars[0], vars[1:]
    Ynode = bn.variable_node(Y)
    if Y in e:
        return Ynode.p(e[Y], e) * enumerate_all(rest, e, bn)
    else:
        return sum(Ynode.p(y, e) * enumerate_all(rest, extend(e, Y, y), bn)
                   for y in bn.variable_values(Y))

#______________________________________________________________________________

enumeration_ask('C', dict(), burglary).show_approx()