Title: A simple Python benchmark exercise
Date: 2018-04-22 15:21

Recently when discussing the Crystal language and
specifically the [Gibbs sample blog post](https://ruivieira.github.io/a-gibbs-sampler-in-crystal.html) with a colleague, he mentioned that the Python benchmark
numbers looked a bit off and not consistent with his experience of numerical
programming in Python.

To recall the numbers:

<table class="table table-hover">
<thead>
  <tr>
    <th>Language</th>
    <th>Time (s)</th>
  </tr>
</thead>
<tbody>
  <tr>
    <td>R</td><td>364.8</td>
  </tr>
  <tr>
    <td>Python</td><td>144.0</td>
  </tr>
  <tr>
    <td>Scala</td><td>9.896</td>
  </tr>
  <tr>
    <td>Crystal</td><td>5.171</td>
  </tr>
  <tr>
    <td>C</td><td>5.038</td>
  </tr>
</tbody>
</table>

To have a better understanding of what is happening, I've decided to profile and benchmark that code (running on Python 3.6).
The code is the following:

```python
import random, math

def gibbs(N=50000, thin=1000):
    x = 0
    y = 0
    print("Iter  x  y")
    for i in range(N):
        for j in range(thin):
            x = random.gammavariate(3, 1.0 / (y * y + 4))
            y = random.gauss(1.0 / (x + 1), 1.0 / math.sqrt(2 * x + 2))
        print(i,x,y)

if __name__ == "__main__":
	gibbs()
```

Profiling this code with `cProfile` gives the following results:

<table class="table table-hover">
<thead>
  <tr>
    <th>Name</th>
    <th>Call count</th>
    <th>Time (ms)</th>
    <th>Percentage</th>
  </tr>
</thead>
<tbody>
  <tr>
    <td>gammavariate</td>
    <td>50000000</td>
    <td>141267</td>
    <td>52.1%</td>
  </tr>
  <tr>
    <td>gauss</td>
    <td>50000000</td>
    <td>65689</td>
    <td>24.2%</td>
  </tr>
  <tr>
 	<td>&ltbuilt-in method math.log&gt</td>
    <td>116628436</td>
    <td>18825</td>
    <td>6.9%</td>
  </tr>
  <tr>
 	<td>&ltmethod 'random' of '_random.Random' objects&gt</td>
    <td>170239973</td>
    <td>17155</td>
    <td>6.3%</td>
  </tr>
  <tr>
 	<td>&ltbuilt-in method math.sqrt&gt</td>
    <td> 125000000 </td>
    <td> 12352 </td>
    <td>4.6%</td>
  </tr>
    <tr>
 	<td>&ltbuilt-in method math.exp&gt</td>
    <td> 60119980 </td>
    <td> 7276 </td>
    <td>2.7%</td>
  </tr>
   <tr>
 	<td>&ltbuilt-in method math.cos&gt</td>
    <td> 25000000 </td>
    <td> 3338 </td>
    <td>1.2%</td>
  </tr>
   <tr>
 	<td>&ltbuilt-in method math.sin&gt</td>
    <td> 25000000 </td>
    <td> 3336 </td>
    <td>1.2%</td>
  </tr>
<tr>
 	<td>&ltbuilt-in method builtins.print&gt</td>
    <td> 50001 </td>
    <td> 1030 </td>
    <td>0.4%</td>
  </tr>
  <tr>
 	<td>gibbs.py</td>
    <td> 1 </td>
    <td> 271396 </td>
    <td>100.0%</td>
  </tr>
</tbody>
</table>

The results look different than the original ones on account of being performed on a different machine. However, we will just look into the relative code performance between different implementations and whether the code itself has room for optimisation.

Surprisingly, the console I/O took a much smaller proportion of the execution time than I expected (0.4%).
On the other hand, as expected, the bulk of the execution time is spent on the `gammavariate` and `normal` methods.
These methods, however, are provided by the Python's standard library `random`, which underneath makes heavy usage of `C` code (mainly by [usage](https://github.com/python/cpython/blob/master/Lib/random.py#L35) of the `random()` function). 

For the second run of the code, I've decided to use `numpy` to sample from the Gamma and Normal distributions. The new code, `gibbs_np.py`, is provided below.

```python
import numpy as np
import math

def gibbs(N=50000, thin=1000):
    x = 0
    y = 0
    print("Iter  x  y")
    for i in range(N):
        for j in range(thin):
            x = np.random.gamma(3, 1.0 / (y * y + 4))
            y = np.random.normal(1.0 / (x + 1), 1.0 / math.sqrt(2 * x + 2))
        print(i,x,y)

if __name__ == "__main__":
	gibbs()
```

We can see from the plots below that the results from both modules are identical.

![Gibbs <>]({filename}/images/gibbs_modules.png)

The profiling results for the `numpy` version were:

<table class="table table-hover">
<thead>
  <tr>
    <th>Name</th>
    <th>Call count</th>
    <th>Time (ms)</th>
    <th>Percentage</th>
  </tr>
</thead>
<tbody>
  <tr>
 	<td>&ltmethod 'gamma' of 'mtrand.RandomState' objects&gt</td>
    <td> 50000000 </td>
    <td> 121211 </td>
    <td>45.8%</td>
  </tr>
  <tr>
 	<td>&ltmethod 'normal' of 'mtrand.RandomState' objects&gt</td>
    <td> 50000000 </td>
    <td> 83092 </td>
    <td>31.4%</td>
  </tr>
  <tr>
 	<td>&ltbuilt-in method math.sqrt&gt</td>
    <td> 50000000 </td>
    <td> 6127 </td>
    <td>2.3%</td>
  </tr>

<tr>
 	<td>&ltbuilt-in method builtins.print&gt</td>
    <td> 50001 </td>
    <td> 920 </td>
    <td>0.3%</td>
  </tr>
  <tr>
 	<td>gibbs_np.py</td>
    <td> 1 </td>
    <td> 264420 </td>
    <td>100.0%</td>
  </tr>
</tbody>
</table>

A few interesting results from this benchmark were the fact that using `numpy` or `random` didn't make much difference overall (264.4 and 271.3 seconds, respectively).
This is despite the fact that, apparently, the Gamma sampling seems to perform better in `numpy` but the Normal sampling seems to be faster in the `random` library.
You will notice that we've still used Python's built-in `math.sqrt` since it is known that for scalar usage it out-performs `numpy`'s equivalent.

Unfortunately, in my view, we are just witnessing a fact of life: _Python is not the best language for number crunching_.

Since the bulk of the computational time, as we've seen, is due to the sampling of the Normal and Gamma distributions, it is clear that in our code there is little room for optimisation except the sampling methods themselves.

A few possible solutions would be to:

 * Convert the code to `Cython`
 * Use FFI to call a highly optimised native library which provides Gamma and Normal distributions (such as [GSL](https://www.gnu.org/software/gsl/))

Nevertheless, personally I still find Python a great language for quick prototyping of algorithms and with an excellent scientific computing libraries ecosystem. Keep on _Pythoning_.
