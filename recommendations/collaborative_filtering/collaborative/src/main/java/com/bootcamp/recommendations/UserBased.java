package com.bootcamp.recommendations;
import java.io.File;
import java.util.List;

import org.apache.mahout.cf.taste.impl.model.file.FileDataModel;

import org.apache.mahout.cf.taste.impl.neighborhood.ThresholdUserNeighborhood;
import org.apache.mahout.cf.taste.impl.neighborhood.NearestNUserNeighborhood;
import org.apache.mahout.cf.taste.impl.recommender.GenericUserBasedRecommender;
import org.apache.mahout.cf.taste.impl.similarity.PearsonCorrelationSimilarity;

import org.apache.mahout.cf.taste.model.DataModel;
import org.apache.mahout.cf.taste.neighborhood.UserNeighborhood;

import org.apache.mahout.cf.taste.recommender.RecommendedItem;
import org.apache.mahout.cf.taste.recommender.UserBasedRecommender;

import org.apache.mahout.cf.taste.similarity.UserSimilarity;
public class UserBased 
{
    public static void main( String[] args )
    {
        try {
          DataModel model = new FileDataModel(new File("/home/nadine/collaborativenotes/book_ratings2.csv"));
          
          //Calculate the similarity between all users
          UserSimilarity similarity = new PearsonCorrelationSimilarity(model);
   
          //Choose the 30 closest neighbors
          UserNeighborhood neighborhood =new NearestNUserNeighborhood(30, similarity, model);  
          UserBasedRecommender recommender = new GenericUserBasedRecommender(model, neighborhood, similarity);   
          
          //Recommend 10 items for user 2391563
          List recommendations = recommender.recommend(2391563, 10);
          for (Object recommendation : recommendations) {
              System.out.println(recommendation);
          }  
        } catch(Exception e) {
              System.out.println("Error :(");
              System.out.println(e.getMessage());
        }
    }
}
