Title: gulp
Date: 2014-07-31 7:52
Category: code

I have been working in a new library called _gulp_ which you can find on [https://github.com/ruivieira/gulp](https://github.com/ruivieira/gulp)

On the project's page there are some usage examples but I will try to summarise the main points here.

The purpose of this library is to facilitate the parallel development of R and Java code, using [rJava](http://cran.r-project.org/web/packages/rJava/index.html) 
as the bridge. Creating bindings in rJava is quite simple, the tricky part of the process (in my opinion) being the 
maintenance of the bindings (usually done by hand) when refactoring your code.
As an example, let's assume you have the following Java class

```$R
@ExportClassReference(value='test')
public class Test {
// Java code
}
```

That you wish to call from R.

