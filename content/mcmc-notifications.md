Title: MCMC notifications
Date: 2015-09-06 11:56
Category: code

It is said that patience is a virtue but the truth is that no one likes waiting
(especially _waiting around_:
[this interesting article](http://www.nytimes.com/2012/08/19/opinion/sunday/why-waiting-in-line-is-torture.html?_r=0)
explores why people prefer walking 8 minutes to the airport’s baggage claim and having the bags ready rather than waiting the same
amount of time entirely in the claim area).

Anyone performing computationally heavy work, such as Monte Carlo methods, will
know that these are usually computationally expensive algorithms which, even
in modern hardware, can result in waiting times in the magnitude of hours,
days and even weeks.
These long running times coupled with the fact that in certain cases it is not
easy to accurately predict how long a certain number of iterations will take,
usually leads to a tiresome behaviour of constantly checking for good (or bad) news.
Although it is perfectly possible to specify that your simulation should stop
after a certain amount of time (especially valid for very long simulations),
this doesn’t seem to be the standard practice.

In this post I’ll detail my current setup for being notified _exactly_ of when
simulations are finished. To implement this setup, the following stack is required:
 
 * A [JDK](http://openjdk.java.net)
 * [Apache Maven](http://maven.apache.org)
 * A messaging service ([Pushbullet](https://www.pushbullet.com)
 * A smartphone, tablet, smartwatch (or any other internet enabled device)

To start, we can create an account in Pushbullet, which will involve, in the
simplest case, signing up using some authentication service such as Google.

Next, we will install the client application (available for
[Android](https://play.google.com/store/apps/details?id=com.pushbullet.android&hl=en_GB),
[iOS](https://itunes.apple.com/gb/app/pushbullet/id810352052)
and [most modern browsers](https://www.pushbullet.com/apps))
after which we can enable notifications (at least in the Android client,
I’m not familiar with the iPhone version).

Since my current work started as a plain Java project which in time evolved mainly
to [Scala](http://scala-lang.org), it consists of an
unholy mixture of Maven as a build tool for Scala code.
This shouldn't be a problem for other setups, but I’ll just go through my specific setup
(_i.e._ using Maven dependencies to a Scala project).


To implement communication between the code and the messaging service,
we can use a simple library such as [jpushbullet](https://github.com/silk8192/jpushbullet).
The library works well enough, although at the time of writing it only supports
Pushbullet’s v1 API but not the [newer v2 API](https://docs.pushbullet.com/#api).
Since the project, unfortunately, is not in Maven central, you should build it from scratch.
Fortunately, in a sensibly configured machine, this is trivial.

In the machine where you plan to perform the simulations, clone and build `jpushbullet`.

```
git clone git@github.com:silk8192/jpushbullet.git
mvn clean install
```

Once the build is complete, you can add it as a local dependency in your project’s `pom.xml`:

```
<dependencies>
  <dependency>
    <groupId>com.shakethat.jpushbullet</groupId>
    <artifactId>jpushbullet</artifactId>
  </dependency>
</dependencies>
```

For the purpose of this example, lets assume that you have the following `Object` as the entry point
of your simulation. The next step is to add a call to the Pushbullet service
before the exit point. Please keep in mind that it is _very bad_ practice to
include your personal API key in your committed code. I _strongly_ suggest you
keep this information in a separate file (_e.g._ in `resources`), read it at
runtime and add it to `.gitignore`.
That being said, place the messaging code as such:

```
package benchmarks

import com.shakethat.jpushbullet.PushbulletClient

object MCMC {

def main(args:Array[String]):Unit = {

  // Your MCMC code

  val client = new PushbulletClient(api_key)
  val devices = client.getDevices
  val title = "MCMC simulation finished"
  val body = "Some summary can be included"
  // n is the preferred device number
  client.sendNote(true, devices.getDevices.get(n).getIden(), title, body)
}

}
```

Usually, I would call this code via `ssh` into my main machine from Maven
(using  [Scala Maven](http://scala-tools.org/mvnsites/maven-scala-plugin/))
as:

```
nohup mvn scala:run -DmainClass=benchmarks.MCMC &
```

Finally, when the simulation is completed, you will be notified in the client
devices (you can select which ones by issuing separate `sendNote` calls)
and include a result summary, as an example.

![Pushbullet <>]({filename}/images/pushbullet.png)

My current setup generates an R script from a template which is run
by `Rscript` in order to produce a PDF report. However, be careful, since file
quotas in Pushbullet are limited, so text notifications should be used
without worry of going over the free usage tier.

Keep in mind, that there are other alternatives to `jpushbullet`, such as
[send-notification](https://github.com/jcgay/send-notification),
a general notification library for Java for which the setup is quite similar.

Hope this was helpful.
