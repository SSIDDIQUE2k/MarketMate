import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import axios from 'axios';

interface SocialMediaPost {
  id: number;
  platform: string;
  content: string;
  media_urls: string[];
  scheduled_time: string;
  status: string;
  metrics: {
    likes: number;
    shares: number;
    comments: number;
    reach: number;
    engagement_rate: number;
  };
  created_at: string;
  updated_at: string;
}

interface SocialMediaAnalytics {
  platform: string;
  followers: number;
  engagement: number;
  reach: number;
  impressions: number;
  period: string;
}

interface SocialMediaState {
  posts: SocialMediaPost[];
  selectedPost: SocialMediaPost | null;
  analytics: SocialMediaAnalytics[];
  loading: boolean;
  error: string | null;
  totalCount: number;
  filters: {
    platform: string;
    status: string;
    search: string;
  };
}

const initialState: SocialMediaState = {
  posts: [],
  selectedPost: null,
  analytics: [],
  loading: false,
  error: null,
  totalCount: 0,
  filters: {
    platform: '',
    status: '',
    search: '',
  },
};

export const fetchPosts = createAsyncThunk(
  'socialMedia/fetchPosts',
  async (params: { page: number; limit: number; filters: SocialMediaState['filters'] }) => {
    const { page, limit, filters } = params;
    const response = await axios.get('/api/social-media/posts/', {
      params: {
        page,
        limit,
        ...filters,
      },
    });
    return response.data;
  }
);

export const fetchPostById = createAsyncThunk('socialMedia/fetchPostById', async (id: number) => {
  const response = await axios.get(`/api/social-media/posts/${id}/`);
  return response.data;
});

export const createPost = createAsyncThunk('socialMedia/createPost', async (post: Partial<SocialMediaPost>) => {
  const response = await axios.post('/api/social-media/posts/', post);
  return response.data;
});

export const updatePost = createAsyncThunk(
  'socialMedia/updatePost',
  async ({ id, data }: { id: number; data: Partial<SocialMediaPost> }) => {
    const response = await axios.patch(`/api/social-media/posts/${id}/`, data);
    return response.data;
  }
);

export const deletePost = createAsyncThunk('socialMedia/deletePost', async (id: number) => {
  await axios.delete(`/api/social-media/posts/${id}/`);
  return id;
});

export const fetchAnalytics = createAsyncThunk(
  'socialMedia/fetchAnalytics',
  async (params: { platform: string; period: string }) => {
    const response = await axios.get('/api/social-media/analytics/', { params });
    return response.data;
  }
);

export const schedulePost = createAsyncThunk(
  'socialMedia/schedulePost',
  async ({ id, scheduledTime }: { id: number; scheduledTime: string }) => {
    const response = await axios.post(`/api/social-media/posts/${id}/schedule/`, { scheduled_time: scheduledTime });
    return response.data;
  }
);

const socialMediaSlice = createSlice({
  name: 'socialMedia',
  initialState,
  reducers: {
    setFilters: (state, action) => {
      state.filters = { ...state.filters, ...action.payload };
    },
    clearFilters: (state) => {
      state.filters = initialState.filters;
    },
    setSelectedPost: (state, action) => {
      state.selectedPost = action.payload;
    },
    clearSelectedPost: (state) => {
      state.selectedPost = null;
    },
  },
  extraReducers: (builder) => {
    builder
      // Fetch Posts
      .addCase(fetchPosts.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(fetchPosts.fulfilled, (state, action) => {
        state.loading = false;
        state.posts = action.payload.items;
        state.totalCount = action.payload.total;
      })
      .addCase(fetchPosts.rejected, (state, action) => {
        state.loading = false;
        state.error = action.error.message || 'Failed to fetch posts';
      })
      // Fetch Post by ID
      .addCase(fetchPostById.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(fetchPostById.fulfilled, (state, action) => {
        state.loading = false;
        state.selectedPost = action.payload;
      })
      .addCase(fetchPostById.rejected, (state, action) => {
        state.loading = false;
        state.error = action.error.message || 'Failed to fetch post';
      })
      // Create Post
      .addCase(createPost.fulfilled, (state, action) => {
        state.posts.unshift(action.payload);
        state.totalCount += 1;
      })
      // Update Post
      .addCase(updatePost.fulfilled, (state, action) => {
        const index = state.posts.findIndex((post) => post.id === action.payload.id);
        if (index !== -1) {
          state.posts[index] = action.payload;
        }
        if (state.selectedPost?.id === action.payload.id) {
          state.selectedPost = action.payload;
        }
      })
      // Delete Post
      .addCase(deletePost.fulfilled, (state, action) => {
        state.posts = state.posts.filter((post) => post.id !== action.payload);
        state.totalCount -= 1;
        if (state.selectedPost?.id === action.payload) {
          state.selectedPost = null;
        }
      })
      // Fetch Analytics
      .addCase(fetchAnalytics.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(fetchAnalytics.fulfilled, (state, action) => {
        state.loading = false;
        state.analytics = action.payload;
      })
      .addCase(fetchAnalytics.rejected, (state, action) => {
        state.loading = false;
        state.error = action.error.message || 'Failed to fetch analytics';
      })
      // Schedule Post
      .addCase(schedulePost.fulfilled, (state, action) => {
        const index = state.posts.findIndex((post) => post.id === action.payload.id);
        if (index !== -1) {
          state.posts[index] = action.payload;
        }
        if (state.selectedPost?.id === action.payload.id) {
          state.selectedPost = action.payload;
        }
      });
  },
});

export const { setFilters, clearFilters, setSelectedPost, clearSelectedPost } = socialMediaSlice.actions;
export default socialMediaSlice.reducer; 