package streaming

import org.apache.spark.SparkConf
import org.apache.spark.streaming.{Seconds, StreamingContext}

object SparkStreaming {

  def updateFunction (newValues: Seq[Int], runningCount: Option[Int]): Option[Int] = {
    val newCount = runningCount.getOrElse(0) + newValues.sum
    Some(newCount)
  }

  def main(args: Array[String]): Unit = {
    if (args.length < 2) {
      System.err.println("Missing arguments")
      System.exit(1)
    }

    //StreamingExamples.setStreamingLogLevels()
    val sparkConf = new SparkConf().setAppName("A3SparkStreaming").setMaster("local[*]")
    // Create the context
    val ssc = new StreamingContext(sparkConf, Seconds(3))
    ssc.checkpoint(".")

    val output_dir = args(1)
    var taskA_dir_count = 1
    var taskB_dir_count = 1
    var taskC_dir_count = 1

    // Create the FileInputDStream on the directory split lines into words
    val lines = ssc.textFileStream(args(0))
    val words = lines.flatMap(_.split(" "))

    //Task 1 - filter and count frequency of words
    val filter_alphanumerical = words.filter(_.forall(_.isLetter))
    val filter_length = filter_alphanumerical.filter(_.length >= 3)
    val wordCounts = filter_length.map(x => (x, 1)).reduceByKey(_ + _)

    //saving to hdfs
    wordCounts.foreachRDD { rdd =>
      if (!rdd.isEmpty()) {
        val taskA_padded_count = "%03d".format(taskA_dir_count)
        val taskA_name = f"$output_dir/taskA-$taskA_padded_count"
        rdd.saveAsTextFile(taskA_name)
        taskA_dir_count += 1
      }
    }


    //Task 2 - count co-occurrence of words
    val pair = lines.flatMap {line =>
      //preprocessing - same as taskA
      val words = line.split(" ")
      val filter_alphanumerical = words.filter(_.forall(_.isLetter))
      val filter_length = filter_alphanumerical.filter(_.length >= 3)
      //create pair words
      val index_words = filter_length.zipWithIndex //create tuple (word,index)
      index_words.flatMap { case (word1, index1) => //unpack tuple
        index_words.filter { case (word2, index2) => index1 != index2 }
          .map{ case (word2,index2) => ((word1,word2),1)}
      }
    }
    val co_occurance = pair.reduceByKey(_+_) //reduce keys

    //Saving to hdfs
    //saves more files than neccessary - for every file there is 3 outputs. i do not know why
    co_occurance.foreachRDD { rdd =>
      if (!rdd.isEmpty()) {
        val taskB_padded_count = "%03d".format(taskB_dir_count)
        val taskB_name = f"$output_dir/taskB-$taskB_padded_count"
        rdd.saveAsTextFile(taskB_name)
        taskB_dir_count += 1
      }
    }
    //Task 3 - UpdateStateByKey


    var runningCounts = co_occurance.updateStateByKey[Int](updateFunction _)
    runningCounts.print()

    runningCounts.foreachRDD { rdd =>
      if (!rdd.isEmpty()) {
        val taskC_padded_count = "%03d".format(taskC_dir_count)
        val taskC_name = f"$output_dir/taskC-$taskC_padded_count"
        rdd.saveAsTextFile(taskC_name)
        taskC_dir_count += 1
      }
    }

    ssc.start()
    ssc.awaitTermination()
    }
}
