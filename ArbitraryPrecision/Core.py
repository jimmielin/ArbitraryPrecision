#########################################################
# com.jimmielin.arbitraryprecision
#--------------------------------------------------------
# ArbitraryPrecision
#
# a simple, efficient arbitrary precision arithmetic library
# for python 3+
# 
# (c) 2018 Haipeng Lin <jimmie.lin@gmail.com>
#
# Originally written for Computational Physics Course
# HW-2, Peking University, School of Physics, Fall 2017
#
#########################################################

class ArbitraryPrecision:
    # Supported maximum precision digits.
    # Set to None for "unlimited" precision, limited only by the properties of the
    # mathematical functions and approximations used in this class.
    # "Unlimited" does not, of course, mean truly unlimited.
    # It is capped at a default of 30-digit precision, which is cut-off when
    # divisions, powers and etc. are performed, which may result in infinite cycling numbers
    # (which we of course cannot store /all/ significant digits for)
    Precision = None

    # Internal Representation of significant digits + sign.
    Base = None

    # Internal Representation of (Integer) Exponent of 10,
    # e.g. 6.283012 = [Base = 6283012, Exponent = 6]
    #      0.097215 = [Base = 97215  , Exponent = -2]
    # This exponent IS the scientific notation exponent.
    # Contrary to intuition, Base * 10eExponent is NOT this number itself.
    # To reconstruct this number, take the first number and insert "." divider in 0-1 pos
    # e.g. 9.7215e-2, this is the actual number.
    # This is implied in later calculations, beware!
    Exponent = 0

    # __init__
    # Initialization Function
    # If a non-integer float type is passed to Base, then this number will be converted
    # to our internal representation.
    #
    # (!!) IF YOU PASS A INTEGER TO BASE there are two possible behaviors.
    # Your int may be interpreted
    # as a literal integer (InternalAware = False) or interpreted as internal representation of significant
    # digits, so 142857 = 1.42857x10^0 = 1.42857.
    # By default, we assume you are NOT aware of the Internal structures. This keeps consistency with float support
    # for base.
    # Set InternalAware = True to interpret as internal representation.
    #
    # (!) Non-Integer Exponents passed to __init__ are currently unsupported.
    def __init__(self, Base, Exponent = 0, InternalAware = False):
        if(not isinstance(Exponent, int)):
            raise ValueError("ArbitraryPrecision: __init__ does not support non-integer exponents")

        if(isinstance(Base, float)):
            # String rep of base, useful for reuse (strings are immutable), also UnSigned variant
            strRep = Base.__str__()
            strRepUS = strRep.replace('-', '')

            # Extract all significant digits
            if('e' in strRep): # Oops, too small; have to expand notation
                # Something like 1e-07... significant digits are before e, then extract the second part and add it to exponent accumulator
                strRepParts = strRep.split('e')
                self.Base = int(strRepParts[0].replace('.', ''))
                Exponent += int(strRepParts[1])
            else:
                self.Base = int(strRep.replace('.', ''))

            # Count exponent for scientific notation
            if(abs(Base) < 1):
                if(strRep == "0.0"):
                    self.Base = 0
                    self.Exponent = 0
                    Exponent = 0
                else:
                    for i in range(len(strRepUS)):
                        if(strRepUS[i] == '.'):
                            continue
                        if(strRepUS[i] != '0'):
                            break

                        Exponent = Exponent - 1
            else:
                Exponent = Exponent - 1 # 1.42857 is 1.425847e0
                for i in range(len(strRepUS)):
                    if(strRepUS[i] == '.'):
                        break
                    Exponent = Exponent + 1

            self.Exponent = Exponent
        else:
            if(Base == 0):
                self.Base = 0
                self.Exponent = 0
            else:
                if(InternalAware):
                    self.Base = Base
                    self.Exponent = Exponent
                else:
                    self.Base = Base
                    self.Exponent = Exponent + len(Base.__str__().replace('-', '')) - 1

        # print("* ArbitraryPrecision: received (Base =", Base, "Exponent =", Exponent.__str__() + ") Interp Base =", self.Base, ", Exp =", self.Exponent)

    ########  Query Functions ########
    # bool isInt
    # Is "Integer"?
    def isInt(self):
        # 123456 (123456, 5)
        return len(self.Base.__str__().replace('-', '')) - 1 == self.Exponent

    ########  Output Functions  ########
    # __repr__
    # Official Object Representation
    def __repr__(self):
        return "ArbitraryPrecision(Base = " + self.Base.__str__() + " Exponent = " + self.Exponent.__str__() + ")"

    # __str__
    # Pretty-Printed Representation of a number
    def __str__(self):
        baseStrRep = abs(self.Base).__str__()
        baseStrRep = baseStrRep[0] + '.' + baseStrRep[1:]
        return ('-' if self.Base < 0 else '') + baseStrRep + "e" + self.Exponent.__str__()

    #########  Modification Functions  ########
    # __neg__
    def __neg__(self):
        return ArbitraryPrecision(Base = (-1) * self.Base, Exponent = self.Exponent, InternalAware = True)

    # __abs__
    def __abs__(self):
        if(self.Base > 0):
            return self
        else:
            return -self

    #########  Comparison Functions  ########
    # __eq__ (self == other)
    def __eq__(self, other):
        if(not isinstance(other, ArbitraryPrecision)):
            return self == ArbitraryPrecision(other)

        return self.Base == other.Base and self.Exponent == other.Exponent

    # __hash__
    # Returns the unique Integer hash of object
    def __hash__(self):
        return hash((self.Base, self.Exponent))

    # __ne__ (self != other)
    def __ne__(self, other):
        return not self == other

    # __lt__ (self < other)
    # Supports comparing with numbers too.
    def __lt__(self, other):
        if(not isinstance(other, ArbitraryPrecision)):
            return self < ArbitraryPrecision(other)

        if(self.Base <= 0 and other.Base > 0):
            return True
        if(self.Base < 0 and other.Base < 0):
            return -other < -self

        # Now they are all positive & same
        if(self.Exponent < other.Exponent):
            return True
        if(self.Exponent > other.Exponent):
            return False

        # Now they're the same exponent
        # You cannot directly compare bases, because they contain precision digits
        # e.g. 1.42857 -> (142857, 0), 1.482562 (1428562, 0)
        # You have to align them and compare, so... the key is to align
        bSelf = self.Base
        bOther = other.Base
        if(len(self.Base.__str__()) < len(other.Base.__str__())):
            bSelf = bSelf * 10**(len(other.Base.__str__()) - len(self.Base.__str__()))
        elif(len(self.Base.__str__()) > len(other.Base.__str__())):
            bOther = bOther * 10**(len(self.Base.__str__()) - len(other.Base.__str__()))

        return bSelf < bOther

    # __le__ (self <= other)
    def __le__(self, other):
        return self == other or self < other

    # __gt__ (self > other)
    def __gt__(self, other):
        return not self < other

    # __ge__ (self >= other)
    def __ge__(self, other):
        return self == other or self > other

    #########  Arithmetic Functions  ########
    # __add__ (self + other)
    def __add__(self, other):
        # To perform arithmetic add, we have to align the bits so that they are
        # aligned to the SMALLEST significant position, e.g.
        # 142.857 (142857, 2) + 3.45678 (345678, 0)
        # MinExpPos: 2-6+1=-3, 0-6+1=-5
        if(not isinstance(other, ArbitraryPrecision)):
            return self + ArbitraryPrecision(other)

        # print(self.__repr__(), other.__repr__())

        # Calculate Minimum Exponents for Alignment
        meSelf  = 1 + self.Exponent - len(self.Base.__str__().replace('-', ''))
        meOther = 1 + other.Exponent - len(other.Base.__str__().replace('-', ''))

        # Save copies of bases
        bSelf   = self.Base
        bOther  = other.Base

        # Borrowed Exponents for Calculation
        bweCalc = max(-meSelf, -meOther)

        # Check which we borrowed, and return to the other
        if(meSelf < meOther):
            bOther = bOther * 10**(meOther + bweCalc)
        else:
            bSelf  = bSelf * 10**(meSelf + bweCalc)

        # # Given minExpPos, e.g. 142.857 is -3, 3.45678 is -5, diff is 2
        # # 14285700 & 345678
        # # 142.85700
        # #   3.45678
        # # ----------

        # # Self's lowest number has a small significant position
        # if(meSelf < meOther):
        #     # Borrow digits to align meOther to all significant digits,
        #     # if it is less than 0.
        #     # TODO: Refactor this code, this if clause is "bad taste"
        #     if(meSelf < 0):
        #         bweCalc = -meSelf
        #         bSelf = bSelf * 10**bweCalcOffset
        #         bOther = bOther * 10**bweCalcOffset

        #     # Now align to the lowest precision counterpart
        #     diff = meOther - meSelf
        #     bOther = bOther * 10**diff # Add "fake" precision digits...
        # else:
        #     if(meOther < 0):
        #         bweCalc = -meOther
        #         bSelf = bSelf * 10**bweCalcOffset
        #         bOther = bOther * 10**bweCalcOffset
            
        #     # Now align to the lowest precision counterpart
        #     diff = meSelf - meOther
        #     bSelf = bSelf * 10**diff # Add "fake" precision digits...

        bSum = bOther + bSelf
        eSum = len(bSum.__str__().replace('-', '')) - 1 - bweCalc
        # print(bSelf, bOther, bSum, eSum, meSelf, meOther, bweCalc)

        # cut Base to target precision
        if(self.Precision != None and len(bSum.__str__()) > self.Precision):
            bSum = int(bSum.__str__()[0:self.Precision])

        result = ArbitraryPrecision(Base = bSum, Exponent = eSum, InternalAware = True)

        # print("=", result.__repr__())

        return result

    # __sub__ (self - other)
    def __sub__(self, other):
        return self + (-other)

    # __mul__ (self * other)
    def __mul__(self, other):
        # To perform arithmetic multiplication, the exponents are multiplied together
        # and the bases are aligned and multiplied together.
        # This means we need to align all problems like this:
        # 1.42951e-5 (142951, -5) x 8.37e4 (837, 4) = 142951 x e(-5-5) x 837 x e(4-2)
        if(not isinstance(other, ArbitraryPrecision)):
            return self * ArbitraryPrecision(other)

        # Calculate "Borrowed" Exponents for Alignment -- always len() - 1 after removing the sign digit
        bweSelf  = len(self.Base.__str__().replace('-', '')) - 1
        bweOther = len(other.Base.__str__().replace('-', '')) - 1

        # Copies of bases
        bSelf    = self.Base
        bOther   = other.Base

        iProduct = bSelf * bOther # this is an INTEGER part, not an actual BASE number!
        # Convert this iProduct to a internal representation
        # Check how many numbers the product can ReTurn to the Exponent (RTE)
        rteProduct = len(iProduct.__str__().replace('-', '')) - 1
        
        # ...and return it
        bProduct = iProduct
        eProduct = self.Exponent + other.Exponent + rteProduct - bweSelf - bweOther

        # cut Base to target precision
        if(self.Precision != None and len(bProduct.__str__()) > self.Precision):
            bProduct = int(bProduct.__str__()[0:self.Precision])

        return ArbitraryPrecision(Base = bProduct, Exponent = eProduct, InternalAware = True)

    # __truediv__ (self / other)
    # Implements "true" division
    def __truediv__(self, other):
        if(not isinstance(other, ArbitraryPrecision)):
            return self / ArbitraryPrecision(other)

        # Calculate "Borrowed" Exponents for Alignment -- always len() - 1 after removing the sign digit
        bweSelf  = len(self.Base.__str__().replace('-', '')) - 1
        bweOther = len(other.Base.__str__().replace('-', '')) - 1
        bwePrecision = 0 # Borrowed Exponent for Precision Division

        # Copies of bases
        bSelf    = abs(self.Base)
        bOther   = abs(other.Base)

        # Until we reach desired precision... or when we have exhausted the divisor
        # The signs are all absolute
        opSelf   = bSelf % bOther
        opResult = (bSelf // bOther).__str__() if bSelf // bOther != 0 else ""
        while(len(opResult.__str__()) < (50 if self.Precision == None else self.Precision) and opSelf != 0):
            opSelf = opSelf * 10
            bwePrecision += 1
            opResult = opResult + (opSelf // bOther).__str__()
            opSelf = opSelf % bOther

        opResult = opResult.lstrip('0')

        if(len(opResult) == 0):
            return ArbitraryPrecision(0)

        bDiv = int(opResult) * (-1 if (self.Base > 0 and other.Base < 0) or (self.Base < 0 and other.Base > 0) else 1)

        rteDiv = len(opResult) - 1

        # print(self, other)
        # print(bSelf, bOther, opSelf, opResult)
        # print(self.Exponent, other.Exponent, rteDiv, bweSelf, bweOther, bwePrecision)
        eDiv = self.Exponent - other.Exponent + rteDiv - bweSelf + bweOther - bwePrecision
        return ArbitraryPrecision(Base = bDiv, Exponent = eDiv, InternalAware = True)

    # __pow__ (self ** other)
    def __pow__(self, other):
        if(not isinstance(other, ArbitraryPrecision)):
            return self ** ArbitraryPrecision(other)

        # Check if other is an "Integer" type in ArbitraryPrecision,
        # as we only support "Integer" types for now.
        # 123456 (123456, 5)
        if(not other.isInt()):
            raise ValueError("ArbitraryPrecision: Currently ** does not support non-integer powers.")
            return NotImplemented
        else:
            rResult = self
            if(other == 0):
                if(self == 0):
                    raise ValueError("ArbitraryPrecision: 0**0 has no mathematical significance")

                return ArbitraryPrecision(1)

            if(other < 0):
                return ArbitraryPrecision(1) / (self ** (-other))
            else:
                for i in range(1, other.Base):
                    rResult = rResult * self
                return rResult

    # sgn(self)
    def sgn(self):
        return self.Base > 0
