# spec/hello_world_spec.py

from mamba import description, it
from expects import expect, equal

def hello_world(name="World"):
    return f"Hello, {name}!"

with description('hello_world function'):
    with it('should greet World by default'):
        result = hello_world()
        expect(result).to(equal("Hello, World!"))
        print("hello")

    with it('should greet custom name'):
        result = hello_world("Alice")
        expect(result).to(equal("Hello, Alice!"))
