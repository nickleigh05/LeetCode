# Inheritance Basics

```python
class Animal:
    def speak(self):
        return "..."

class Dog(Animal):              # Dog inherits from Animal
    def speak(self):             # overrides the parent's method
        return "Woof"

Dog().speak()      # "Woof"
```

A subclass `Dog(Animal)` gets all of `Animal`'s methods/attributes for free, and can override any of them by redefining the method with the same name. Rare in interview-style LeetCode solutions but shows up in "design" problems built on a shared base structure.

**Related:** [class-basics](class-basics.md) · [dunder-methods](dunder-methods.md)
