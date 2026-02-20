# Testing Driven Development

This repo started as an implementation of something that I've been thinking about
for a while: a flexible graph process in Python. It is more _for fun_ than because
there are not good libraries for this already.

I decided to do it while reading _Clean Code_. I've been thinking about testing
driven development, but I didn't really know how to do it. I came across these
three rules in _Clean Code_ (paraphrasing):
1. Don't write code until you have written a minimal test of the code.
2. Don't write mode tests than are needed for tests to fail.
3. Don't write more code than is needed to pass failing tests.

Take as a group, we get can see an outline of a process. Let's a another principle:

> I. Single Purpose. A class should have one responsibility; a function should do
one thing.

When we combine these, a process for writing code emerges.

Biographical digression: I love process, axioms, and princples. Codifying makes
me happy. It's not because codifying typically gets it right. Codifying is hard.
My Ph.D. is in philosophy, and a lot of history of philosophy can be see as an
attempt to codify. A principle to be aware of:

II. Without good judgement, every good principle can lead you astray.

II is reflexive. This history of philosophy might be seen as an attempt to
say what is good judgement. The success of philosophy might make you think this is
impossible. My own sense is that it is more like mathematics that you think:
any system capable of delivering only truths cannot deliver all the truths.
End digression.

So, I decided to try applying these rules for a project. Let's do 1,2 and 3.
I also decided to emphasize some other clean code rules, especially, short
functions.
Let's make some observations about the results.

## Benefits

The test coverage ended up very good. There's not much more to say here.
There are a lot of tests. They check methods to see that they work. All the tests
are passing and I'm confident in this code.

It made me think about edge cases. This is a collateral benefit. When you
are thinking about the test, you are thinking about what the result will be. You
are thinking about the requirements of the code. You are thinking about what you
need to accomplish. It felt a few times like I noticed something that I needed
because of the process.

It helped me to write single purpose functions. Here' an example. I needed a
traversal algorithm for a basic graph. So, I started writing a DFS method. I
started with a DFS that took one optional argument (which node to start from).
(This felt a little off from the get go, but Python does love optional arguments.)
I noticed almost immediately that these are two purposes: reaching every node
accessible from a given node is not the same as reaching every node. I ended up
breaking the function up.

It helped me break functionality into parts. We're continuing the tale of the
DFS: a traversal amounts to (1) reach every node accessible from an arbitrary node;
(2) if there are untraversed nodes, pick an arbitrary one and do (1); (3) repeat
until there are no untraversed nodes.
The method of reaching every node from a given node is (1). Now, we just do (1)
in a loop that matches 2 and 3.

It was easy to refactor. A few times I decide to rework something. I added a
`disconnet` method to my Node class. The purpose of the method was to remove
all edge from that node to a selected edge node. I decided that this was more
of an operation for graphs than for nodes. The refactor felt very quick.
I deleted the method from Node. I ran all my tests. I looked at what failed and
why. I had a two things to do: remove the test of the method; fix the `remove_node`
method of graph, which depended on it. What I didn't have to do was _think hard
about the dependencies in the system to fix all the things I just broke._ The
tests exposed all that for me.

Keep the implementation simple. Following the rule of "don't write more than you
need to to pass the test" helped me not get complex. Should I cash this call
to make sure that we're not looping every edge in the node over an over? Since
the test did not cover that question, I didn't write code to cover it. I have
to circle back to the refactor now. Let's supposed that I do want to refactor
and add a cache: I already have a test of the basic function of the method.
Adding a cache should definitely not break that test. I just need to write a test
which shows that a change which invalidates the cache will produce the desired
outcome. Then I add the cache, run my tests and smile (or fix whatever I did wrong.)

## Costs

Sometimes  I landed outside the circle of the process. Let's go back to the case of the disconnet method I refactored. I wanted to get rid of it. Here's a failing test:
`assert not hasattr(node, 'disconnect')`. But let's face it, this isn't a good
test. It's not a _bad_ test. It's a test which is going to be really confusing
to the person who reads it three months from now. What is thing not in this name space?
Why are we assuring that it does not have this name? Does this _almost_ implement
some interface that we don't want it to have? Etc.

Besides, it's literally impossible
to make this change (remove `disconnect`) without causing a test to fail.
At this point, I wanted to extend 1-3. But really, we needed a principle for
removing tests and deleting code. These aren't covered and it's not totally obvious
to me how those fit in the 1-3 cycle. A point (_the_ point?) of TDD is to make
sure you have test coverage--so how to you decide when a test is stale.
I can say, at this point, I'm pretty confident that an important component of
thinking about tests is missing from 1-3.

Another thing that stood out to me: what if you missed a case? What if you're
still learning (we are _all_ still learning) and you don't yet know all the tests
you need? The illusion of coverage is dangerous. I can definitely see how this
process isn't a panacea. You still need good reviewers who can make sure that
you have covered all the cases for your code. You still need to think hard about
what the requirements are. You could definitly get in a rush, look like you have
been totally TDD, and produce tests that don't cover you.

What I just said is damned issue with code. Methodologies only go so
far. My little experiment writing a graph with 1-3 made me feel good about this
methodology. While a methodology can never force you to practice it well, I ~will
say that~ have already said that thinking about tests helped me to think about
the requirements of the code, helped me start simple, and set me up to refactor.
Really, I'm not sure there's more you could ask for from a methodology: set me
up to write good code, set me up to fix it.

If you don't write good tests....

## Reflections


Single purpose and indirections.
Memory and trust.
Single purpose and requirements. When reqs change, single purpose functions don't.
Multipurpose functions do.

I feel like I've encountered the idea that good code is easy to test. That feels
pretty true to me; or, if you mean "code that's easy to extendable, reliable and
maintable is easy to test", I would say "I'm not sure about that, but I will bet
it's _easier_ to test than it's alternative." This is my intuition. I'm not a
junior dev anymore, but I don't have enough experience to be a lead either.

But I will say that code which is easy to test is not necessarily good.
You could write a class that's easy to test. Then you could write another class
that's easy to test. And you could write some integration tests for the two.
But if these class are bad, you will eventually find yourself stuck. You will
not be able to extend them further without refactoring them. And, once you have
depended upon them, you will probably find the refactor very messy. You will
probably find yourself doing a pretty big teardown. Bad code can be easy to test.
You might say "bad code is easy to test until it isn't." Sure. But the point of a
methodology is not that I can follow until I can't. Tests just aren't the sole
measure of code; you can't guarantee that focusing on tests will get the job done
forever. Or, "Without good judgement, every good principle can lead you astray."

Proof versus test. Am I getting too philosophical here? It's a debate as old as
Plato and Aristotle. Some people want proofs. Some people was verifications.
Rationalism and empiricism. Tests verify your code, but like all empirical results
it is _possible_ that some unforeseen case has eluded the test. (See comments
on illusions of coverage above.) I write a lot of data sciency code. I have to
test whether some input function that handles arbitrary arrays returns the expected
outputs. So I have some guiding principles: test the empty array; test 1xn arrays,
test nx1 arrays, test n x m arrays for three cases: n > m, n = m, n < m. But there's
more: test arrays that are not sorted, test sorted arrays; test reverse sorted arrays, test arrays that are all the same value, test arrays with redundant values; test
them where there redundant values are side-by-side and where they are not
side-by-side. Oh, did I mention that arrays can be arbitrarily larger than
2 dimensions? Ho. Lee. Shit.

At this point, we want something like proof: if n passes then n + 1 will pass and
for some arbitrary n, n passed. (Mathematical induction.) The test I wrote for
this project fall short of this standard. I have a topological sort algorithm.
I have a mental check that it is correct for arbitrary cases. I have what _I'm
confident_ implements the algorithm in code. I have a test for an acyclic graph
(4 nodes) that passes and a test that it will raise if it has a cycle. There's
another test if it has an island (a node not reachable from some other node.)
_Should_ I be confident?

Another theme of philosophy (neither rationalist nor
empiricist) is that progress is iterative, we rebuild our ship at sea. We know
at all stages that it is not perfect. A good contrivance would be if we could
rebuild quickly and without creating problems in the process. Yet another,
progress is collective, collaborative.
