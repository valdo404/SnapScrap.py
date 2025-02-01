ThisBuild / scalaVersion := "2.13.10"
ThisBuild / organization := "org.levaldo"

lazy val root = (project in file("."))
  .settings(
    name := "snapscrap",
    version := "0.1.0",
    
    libraryDependencies ++= Seq(
      "com.google.cloud.functions" % "functions-framework-api" % "1.1.0",
      "io.cloudevents" % "cloudevents-api" % "2.5.0",
      "io.cloudevents" % "cloudevents-core" % "2.5.0",
      "io.cloudevents" % "cloudevents-json-jackson" % "2.5.0",
      "com.google.cloud" % "google-cloud-pubsub" % "1.123.17",
      "com.google.code.gson" % "gson" % "2.10.1",
      "org.slf4j" % "slf4j-api" % "2.0.9",
      "ch.qos.logback" % "logback-classic" % "1.4.11" % Runtime
    ),

    assembly / assemblyMergeStrategy := {
      case PathList("META-INF", xs @ _*) => MergeStrategy.discard
      case x => MergeStrategy.first
    }
  )
