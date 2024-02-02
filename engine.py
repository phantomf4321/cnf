class CNF:




  def __init__(self, formula):
      self.formula = formula




  # Reduces the operators, if "\Wedge" is present inside "\Wedge" or "\Vee" inside "\Vee"
  # Example : ["\Wedge", "A", ["\Wedge", "B", "C"]] should be ["\Wedge", "A", "B", "C"]
  def reduceOperators(self, formula):
      if (isinstance(formula, str)):
          return formula
      operator = formula[0]
      literals = []
      propositions = []
      for index, item in enumerate(formula):
          if (index > 0):
              if (isinstance(item, str)):
                  literals.append(item)
              elif (isinstance(item, list)):
                  propositions.append(self.reduceOperators(item))
      newFormula = literals
      for item in propositions:
          if (isinstance(item, list) and item[0] == operator):
              for i, clause in enumerate(item):
                  if (i > 0):
                      newFormula.append(clause)
          else:
              newFormula.append(item)
      newFormula.insert(0, operator)
      return newFormula




  # Removes duplicate elements from "\Wedge" and "\Vee"
  # Example : ["\Wedge", "A", "A"] should be "A"
  def removeDuplicates(self, formula):
      if (isinstance(formula, str) or (
              isinstance(formula, list) and formula[0] == "\~" and isinstance(formula[1], str))):
          return formula
      for i, checkItem in enumerate(formula):
          if (i > 0):
              for j, item in reversed(list(enumerate(formula))):
                  if (j > i):
                      if (isinstance(item, list)):
                          newItem = self.removeDuplicates(item)
                          formula.insert(j, newItem)
                          formula.remove(item)
                      if (checkItem == item):
                          formula.remove(item)
      if (isinstance(formula, list) and formula[0] != "\~" and len(formula) < 3):
          return formula[1]
      return formula




  # Sorts the literals and lists in the formula (will be used for removing duplicate items in list)
  # The literals are in the beginning followed by lists. And the "\Wedge" list is present in the end
  def sort(self, formula):
      if (isinstance(formula, str)):
          return formula
      operator = formula[0]
      if (operator == "\Rightarrow"):
          return formula
      literals = []
      propositions = []
      for index, item in enumerate(formula):
          if (index > 0):
              if (isinstance(item, str)):
                  literals.append(item)
              elif (isinstance(item, list)):
                  propositions.append(self.sort(item))
      if (len(literals) > 0):
          literals.sort()
      if (len(propositions) > 0):
          propositions = sorted(propositions, key=lambda proposition: proposition[0], reverse=True)
      newFormula = literals + propositions
      newFormula.insert(0, operator)
      return newFormula




  # Converts to CNF by taking different cases separately
  def convert(self, formula):
      if (isinstance(formula, str)):
          return formula
      elif (isinstance(formula, list)):
          # A => B    --->    ~A | B
          if (formula[0] == "\Rightarrow"):
              return self.convert(["\Vee", self.convert(["\~", self.convert(formula[1])]), self.convert(formula[2])])
          # A <=> B   --->    (~A | B) & (A | ~B)
          elif (formula[0] == "\Leftrightarrow"):
              return self.convert("\Wedge", self.convert(["\Vee", self.convert(["\~", formula[1]]), formula[2]]),
                             self.convert(["\Vee", formula[1], self.convert(["\~", formula[2]])]))
          elif (formula[0] == "\~"):
              # ~p
              if (isinstance(formula[1], str)):
                  return formula
              # ~~p   --->    p
              elif (isinstance(formula[1], list) and (formula[1])[0] == "\~"):
                  return self.convert((formula[1])[1])
              # ~(A & B & C & ...)  --->    ~A | ~B | ~C | ....
              elif (isinstance(formula[1], list) and (formula[1])[0] == "\Wedge"):
                  disjuncts = []
                  for index, item in enumerate(formula[1]):
                      if (index > 0):
                          disjuncts.append(self.convert(["\~", item]))
                  disjuncts.insert(0, "\Vee")
                  return self.convert(disjuncts)
              # ~(A | B | C | ...)  --->    ~A & ~B & ~C & ....
              elif (isinstance(formula[1], list) and (formula[1])[0] == "\Vee"):
                  conjuncts = []
                  for index, item in enumerate(formula[1]):
                      if (index > 0):
                          conjuncts.append(self.convert(["\~", item]))
                  conjuncts.insert(0, "\Wedge")
                  return self.convert(conjuncts)
              # ~(A => B) --->   A & ~B
              elif (isinstance(formula[1], list) and ((formula[1])[0] == "\Rightarrow")):
                  return self.convert(["\Wedge", self.convert((formula[1])[1]), ["\~", self.convert((formula[1][2]))]])
              elif (isinstance(formula[1], list) and (formula[1])[0] == "\Leftrightarrow"):
                  return self.convert(["\~", self.convert(formula[1])])
          elif (formula[0] == "\Vee"):
              # A | A  --->    A
              formula = self.sort(formula)
              formula = self.removeDuplicates(formula)
              # Handling the case ["\Vee", "A", ["\Vee", "B", "C"]]
              formula = self.reduceOperators(formula)
              # The order will be messed up when the redundant operators are removed
              # Handling the case when the formula is reduced.
              # For instance A or A is reduced to A
              formula = self.sort(formula)
              if (len(formula) == 1):
                  return formula
              if ((isinstance(formula[-1], list) and (formula[-1])[0] == "\Wedge")):
                  # A | (B & C & D & ...)  --->  (A | B) & (A | C) & (A | D) & ...
                  conjuncts = []
                  for i, item in enumerate(formula[-1]):
                      if (i > 0):
                          conjuncts.append(["\Vee", formula[-2], item])
                  conjuncts.insert(0, "\Wedge")
                  # If only 2 items, then remove them and also remove OR
                  if (len(formula) < 4):
                      return self.convert(conjuncts)
                  else:
                      formula.remove(formula[-1])
                      formula.remove(formula[-1])
                  formula.append(conjuncts)
                  return self.convert(formula)
              # Case A OR B,
              elif ((isinstance(formula[1], str) and isinstance(formula[2], str)) or (
                      isinstance(formula[1], str) and isinstance(formula[2], list) and (formula[2])[
                  0] == "\~" and isinstance((formula[2])[1], str)) or (
                            isinstance(formula[2], str) and isinstance(formula[1], list) and (formula[1])[
                        0] == "\~" and isinstance((formula[1])[1], str))):
                  formula.append(["\Vee", formula[1], formula[2]])
                  formula.remove(formula[1])
                  formula.remove(formula[1])




                  formula = self.reduceOperators(formula)
                  formula = self.sort(formula)
                  return formula
              # Case !A OR !B
              elif (isinstance(formula[1], list) and (formula[1])[0] == "\~" and isinstance((formula[1])[1],
                                                                                             str) and isinstance(
                      formula[2], list) and (formula[2])[0] == "\~" and isinstance((formula[2])[1], str)):
                  return formula
              # For any other operator compute the inner operator after or
              else:
                  disjuncts = []
                  for i, item in enumerate(formula):
                      if (i > 0):
                          disjuncts.append(self.convert(item))
                  disjuncts.insert(0, "\Vee")
                  return self.convert(disjuncts)




          elif (formula[0] == "\Wedge"):
              # Handling the case ["\Wedge", "A", ["\Vee", "C", "D"], ["\Vee", "D", "C"]]
              formula = self.sort(formula)
              formula = self.removeDuplicates(formula)
              # Handling the case ["\Wedge", "A", ["\Wedge", "B", "C"]]
              formula = self.reduceOperators(formula)
              # The order will be messed up when the redundant operators are removed
              formula = self.sort(formula)
              if (len(formula) == 1):
                  return formula
              disjuncts = []
              for i, item in enumerate(formula):
                  if (i > 0):
                      disjuncts.append(self.convert(item))
              disjuncts.insert(0, "\Wedge")




              disjuncts = self.reduceOperators(disjuncts)
              return disjuncts





