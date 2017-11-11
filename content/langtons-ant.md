Title: Langton's Ant
Date: 2016/06/23 21:55
Category: code
JavaScripts: ants.js
Author: Rui Vieira

Last week, at the [North East Functional Programming](https://twitter.com/FP_North_East)
meet up, we were given a code Kata consisting of the
[Langton's ant](https://en.wikipedia.org/wiki/Langton%27s_ant) algorithm.
I've had a go at Scala but decided later on to put a live version in this blog.
I considered several implementation options, such as scala.js and Elm, but in the end
decided to implement it in plain Javascript.

<div style="margin-left: 10%;margin-right: 10%;">
  <canvas id="ants" width="640" height="480"></canvas>
</div>

<button type="button" class="btn btn-secondary btn-sm" id="addAntButton">Add ant</button>
