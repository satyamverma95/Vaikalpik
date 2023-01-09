import read, copy
from util import *
from logical_classes import *

verbose = 0

class KnowledgeBase(object):
    def __init__(self, facts=[], rules=[]):
        self.facts = facts
        self.rules = rules
        self.ie = InferenceEngine()

    def __repr__(self):
        return 'KnowledgeBase({!r}, {!r})'.format(self.facts, self.rules)

    def __str__(self):
        string = "Knowledge Base: \n"
        string += "\n".join((str(fact) for fact in self.facts)) + "\n"
        string += "\n".join((str(rule) for rule in self.rules))
        return string

    def _get_fact(self, fact):
        """INTERNAL USE ONLY
        Get the fact in the KB that is the same as the fact argument

        Args:
            fact (Fact): Fact we're searching for

        Returns:
            Fact: matching fact
        """
        for kbfact in self.facts:
            if fact == kbfact:
                return kbfact

    def _get_rule(self, rule):
        """INTERNAL USE ONLY
        Get the rule in the KB that is the same as the rule argument

        Args:
            rule (Rule): Rule we're searching for

        Returns:
            Rule: matching rule
        """
        for kbrule in self.rules:
            if rule == kbrule:
                return kbrule

    def kb_add(self, fact_rule):
        """Add a fact or rule to the KB
        Args:
            fact_rule (Fact or Rule) - Fact or Rule to be added
        Returns:
            None
        """
        printv("Adding {!r}", 1, verbose, [fact_rule])
        if isinstance(fact_rule, Fact):
            if fact_rule not in self.facts:
                self.facts.append(fact_rule)
                for rule in self.rules:
                    self.ie.fc_infer(fact_rule, rule, self)
            else:
                if fact_rule.supported_by:
                    ind = self.facts.index(fact_rule)
                    for f in fact_rule.supported_by:
                        self.facts[ind].supported_by.append(f)
                else:
                    ind = self.facts.index(fact_rule)
                    self.facts[ind].asserted = True
        elif isinstance(fact_rule, Rule):
            if fact_rule not in self.rules:
                self.rules.append(fact_rule)
                for fact in self.facts:
                    self.ie.fc_infer(fact, fact_rule, self)
            else:
                if fact_rule.supported_by:
                    ind = self.rules.index(fact_rule)
                    for f in fact_rule.supported_by:
                        self.rules[ind].supported_by.append(f)
                else:
                    ind = self.rules.index(fact_rule)
                    self.rules[ind].asserted = True

    def kb_assert(self, fact_rule):
        """Assert a fact or rule into the KB

        Args:
            fact_rule (Fact or Rule): Fact or Rule we're asserting
        """
        printv("Asserting {!r}", 0, verbose, [fact_rule])
        self.kb_add(fact_rule)

    def kb_ask(self, fact):
        """Ask if a fact is in the KB

        Args:
            fact (Fact) - Statement to be asked (will be converted into a Fact)

        Returns:
            listof Bindings|False - list of Bindings if result found, False otherwise
        """
        #print("Asking {!r}".format(fact))
        if factq(fact): #isinstance(fact, Fact):
            f = Fact(fact.statement)
            bindings_lst = ListOfBindings()
            # ask matched facts
            for fact in self.facts:
                #print ("Sending data to match f.statement", f.statement)
                #print("Sending data to match fact.statement", fact.statement)
                binding = match(f.statement, fact.statement)
                if binding:
                    bindings_lst.add_bindings(binding, [fact])

            return bindings_lst if bindings_lst.list_of_bindings else []

        else:
            print("Invalid ask:", fact.statement)
            return []

    def kb_retract(self, fact_rule):
        """Retract a fact or a rule from the KB

        Args:
            fact_rule (Fact or Rule) - Fact or Rule to be retracted

        Returns:
            None
        """
        printv("Retracting {!r}", 0, verbose, [fact_rule])
        ####################################################
        # Student code goes here
        #print("Retracting Fact ", fact_rule)
        ##print("Knowledge Base Status - Facts ", self.facts)
        #print("Knowledge Base Status - Rule ", self.rules)

        if factq(fact_rule):

            is_asserted = fact_rule.asserted
            supported_by_f_r = fact_rule.supported_by
            supports_f = fact_rule.supports_facts
            supports_r = fact_rule.supports_rules

            if(is_asserted):

                #Simple case where facts didn't have any support either by rule or facts.
                #Case-1 : Asserted facts and rules that DO NOT have support can be retracted.
                #if ( not supported_by_f_r ) and ( not supports_f ) and ( not supports_r ):
                if (not supported_by_f_r) :
                    self.facts.remove(fact_rule)
                elif ( supported_by_f_r  ):  ## Case-2 : Asserted facts and rules that have support cannot be retracted; when attempted to be retracted, they can and should only be unasserted.
                    ind = self.facts.index(fact_rule)
                    self.facts[ind].asserted = False

            else:

                ## Case -3 : Inferred facts and rules that DO NOT have support shouldn’t even be existing and they should have been retracted when their supports were retracted.
                if (supported_by_f_r) and (not supports_f) and (not supports_r):

                    should_be_deleted_f = False
                    should_be_deleted_r = False

                    for f_r in fact_rule.supported_by:

                        if (factq(f_r) ):
                            if ( f_r not in self.facts ):
                                should_be_deleted_f = True
                        else:
                            if (f_r not in self.rules):
                                should_be_deleted_r = True

                    if ( ( should_be_deleted_f ) or ( should_be_deleted_r ) ):
                        self.facts.remove(fact_rule)

        else :  #For Removing Rules

            is_asserted = fact_rule.asserted
            supported_by_f_r = fact_rule.supported_by
            supports_f = fact_rule.supports_facts
            supports_r = fact_rule.supports_rules

            if (is_asserted):

                # Simple case where facts didn't have any support either by rule or facts.
                #case - 1 : Asserted facts and rules that DO NOT have support can be retracted
                if (not supported_by_f_r) and (not supports_f) and (not supports_r):
                    self.rules.remove(fact_rule)
                elif (supported_by_f_r):  ## Case - 2 :  Asserted facts and rules that have support cannot be retracted; when attempted to be retracted, they can and should only be unasserted.
                    ind = self.rules.index(fact_rule)
                    self.rules[ind].asserted = False

            else:

                if (not supported_by_f_r) and (not supports_f) and (not supports_r):

                    should_be_deleted_f = False
                    should_be_deleted_r = False

                    for f_r in fact_rule.supported_by:

                        if (factq(f_r)):
                            if (f_r not in self.facts):
                                should_be_deleted_f = True
                        else:
                            if (f_r not in self.rules):
                                should_be_deleted_r = True

                    if ((should_be_deleted_f) or (should_be_deleted_r)):
                        self.facts.remove(fact_rule)


class InferenceEngine(object):
    def create_statement ( self, rule_rhs, bindings ):

        #print("RHS Rule", rule_rhs)
        #print("RHS Rule", type(rule_rhs))
        #print("RHS Rule Statement", rule_rhs.terms)
        #print("RHS Rule Statement", rule_rhs.predicate)
        #print("RHS Rule Statement - 1", type(rule_rhs.terms[0].term.element))
        #print("RHS Rule Statement - 1", type(rule_rhs.terms[1].term.element))
        #print("Bindings Received", bindings)

        new_fact = 'fact: '
        new_fact += '(' + rule_rhs.predicate + ' '

        for term in rule_rhs.terms :
            var_const = term.term.element
            if( var_const in bindings.bindings_dict.keys() ):
                new_fact += bindings.bindings_dict[ var_const ] + ' '

        new_fact += ')'

        #print("New Fact Found", new_fact)
        return ( new_fact )





    def fc_infer(self, fact, rule, kb):
        """Forward-chaining to infer new facts and rules

        Args:
            fact (Fact) - A fact from the KnowledgeBase
            rule (Rule) - A rule from the KnowledgeBase
            kb (KnowledgeBase) - A KnowledgeBase

        Returns:
            Nothing
        """
        printv('Attempting to infer from {!r} and {!r} => {!r}', 1, verbose,
            [fact.statement, rule.lhs, rule.rhs])
        ####################################################
        # Student code goes here
        # fact_1 = type(fact)
        # rule_1 = type(rule)
        # print ( "In fc_infer - Fact ", fact )
        # print ( "In fc_infer - Rule - LHS ", rule.lhs[0] )
        # print ( "In fc_infer - Rule - RHS ", rule.rhs )

        new_fact_f = ''
        #print("Inferring New Rules for fact and Rules", fact, rule)
        bindings = match(fact.statement, rule.lhs[0])

        if (bindings):

            if (len(rule.lhs) == 1):

                # print("Bindings Received", (bindings.bindings_dict))
                # print("Bindings Received", (bindings.bindings))
                # print("Bindings Received", type(bindings))

                # new_fact_statement = self.create_statement ( rule.rhs, bindings )
                new_fact_statement = instantiate(rule.rhs, bindings)
                #print("New Fact Statement ", new_fact_statement)
                new_fact_f = Fact(new_fact_statement, [[fact], [rule]])
                # new_fact_f = read.parse_input( new_fact_statement, [[fact], [rule]] )
                fact.supports_facts.append(new_fact_f)
                rule.supports_facts.append(new_fact_f)

                # print("New Fact ", Fact(new_fact, [fact, rule]) )
                # print( "Facts and Bool Before Adding", new_fact_f, bindings_bool)

                if (isinstance(new_fact_f, Fact) or isinstance(new_fact_f, Rule)):
                    kb.kb_assert(new_fact_f)

                    # input to Fact " motherof ada bing " Then it will convert to statement format
                    # Input to Fact " fact.statement"
            else:
                new_fact_statement_lhs = list()

                for rule_lhs in rule.lhs[1:]:
                    new_fact_statement_lhs.append(instantiate(rule_lhs, bindings))
                    #print("Unified Statement Received lhs", new_fact_statement_lhs)

                new_fact_statement_rhs = instantiate(rule.rhs, bindings)
                #print("Unified Statement Received rhs", new_fact_statement_rhs)
                # print("New Fact Statement ", new_fact_statement)
                new_rule = Rule([new_fact_statement_lhs, new_fact_statement_rhs], [[fact], [rule]])
                # new_fact_f = read.parse_input( new_fact_statement, [[fact], [rule]] )
                #print("New Rule Revceived ", new_rule)


                #rule.supports_rules.append(new_rule)
                fact.supports_rules.append(new_rule)

                # print("New Fact ", Fact(new_fact, [fact, rule]) )
                # print( "Facts and Bool Before Adding", new_fact_f, bindings_bool)

                if (isinstance(new_rule, Rule)):
                    kb.kb_assert(new_rule)
