Title: t as mixture of Normals
Date: 2016-11-27 14:00
Category: statistics, code
Tags: statistics

(Based on Rasmus Bååth's [post](http://www.sumsar.net/blog/2013/12/t-as-a-mixture-of-normals/))

A scaled $t$ distribution, with $\mu$ mean, $s$ scale and $\nu$ degrees of freedom, can be simulated 
from a mixture of Normals with $\mu$ mean and precisions following a Gamma distribution:

\begin{align}
y &\sim \mathcal{N}\left(\mu,\sigma\right) \\
\sigma^2 &\sim \mathcal{IG}\left(\frac{\nu}{2},s^2\frac{\nu}{2}\right)
\end{align}

Since I've recently pickep up again the [crystal-gsl](https://github.com/ruivieira/crystal-gsl) in
my spare time, I've decided to replicate the previously mentioned post using a Crystal one-liner. To simulate 10,000 samples from 

$t_2\left(0,3\right)$ using the mixture, we can then write:

```
samples = (0..10000).map { |x| 
 Normal.sample 0.0, 1.0/Math.sqrt(Gamma.sample 1.0, 9.0) 
}
```

We can see the mixture distribution (histogram) converging nicely to the $t_2(0,3)$ (red):

{% video {filename}/images/t_mixture.mp4 600 400 %}